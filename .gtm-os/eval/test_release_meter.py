"""Focused accounting regressions; run directly with Python, no extra dependencies."""
import copy
import unittest
import release_meter as meter


class ReleaseMeterTests(unittest.TestCase):
    def run_input(self, count=5):
        expected = {f'G{i}': True for i in range(1, count + 1)}
        run = meter.template(expected, 'suite')
        run.update(candidate='candidate-sha+overlay-sha', client='test-client', model='test-model', bootstrap='PASS')
        for row in run['cases']:
            row.update(objective='PASS', judge='PASS', evidence='captured objective and independent Judge')
        for check in run['safety'].values():
            check.update(status='PASS', evidence='captured safety proof')
        return run, expected

    def evaluate(self, run, expected):
        return meter.score(run, expected, 'suite')

    def test_exact_eighty_percent_meets_target_with_advisory_findings(self):
        run, expected = self.run_input()
        run['cases'][0]['objective'] = 'FAIL'
        run['consistency'] = [{'severity': 'HIGH', 'finding': 'Known instruction contradiction'}]
        result = self.evaluate(run, expected)
        self.assertEqual((result['verdict'], result['adherence_percent']), ('READY', 80))
        self.assertEqual(len(result['consistency_advisory']), 1)

    def test_below_target_is_review_not_safety_block(self):
        run, expected = self.run_input(7)
        for row in run['cases'][:2]:
            row['judge'] = 'FAIL'
        result = self.evaluate(run, expected)
        self.assertEqual(result['verdict'], 'REVIEW')
        self.assertEqual(result['first_attempt_passes'], 5)

    def test_retry_pass_does_not_replace_first_attempt(self):
        run, expected = self.run_input()
        row = run['cases'][0]
        row['retry'] = copy.deepcopy(row)
        row['objective'] = 'FAIL'
        self.assertEqual(self.evaluate(run, expected)['first_attempt_passes'], 4)

    def test_invalid_case_exposes_incomplete_coverage_not_success(self):
        run, expected = self.run_input()
        run['cases'][0].update(validity='HARNESS_ERROR', objective='FAIL', evidence='independent runtime failure')
        result = self.evaluate(run, expected)
        self.assertEqual((result['adherence_percent'], result['coverage_percent']), (100, 80))
        self.assertEqual((result['target_status'], result['verdict']), ('INCOMPLETE', 'REVIEW'))

    def test_missing_required_judge_is_not_a_pass(self):
        run, expected = self.run_input()
        run['cases'][0]['judge'] = 'NOT_REQUIRED'
        self.assertEqual(self.evaluate(run, expected)['valid_completed'], 4)

    def test_every_safety_failure_and_missing_check_blocks_perfect_score(self):
        for name in meter.SAFETY:
            for status in ('FAIL', 'NOT_RUN'):
                with self.subTest(name=name, status=status):
                    run, expected = self.run_input()
                    run['safety'][name]['status'] = status
                    self.assertEqual(self.evaluate(run, expected)['verdict'], 'BLOCKED')

    def test_applicable_safety_cannot_be_marked_not_applicable(self):
        for name in ('privacy', 'delivered_output_contract'):
            run, expected = self.run_input(7)
            run['safety'][name]['status'] = 'NOT_APPLICABLE'
            with self.assertRaises(ValueError):
                self.evaluate(run, expected)

    def test_missing_duplicate_unknown_cases_rejected(self):
        for change in ('drop', 'duplicate', 'unknown'):
            run, expected = self.run_input()
            if change == 'drop':
                run['cases'].pop()
            elif change == 'duplicate':
                run['cases'].append(copy.deepcopy(run['cases'][0]))
            else:
                run['cases'][0]['id'] = 'G999'
            with self.subTest(change=change), self.assertRaises(ValueError):
                self.evaluate(run, expected)

    def test_suite_change_cannot_be_silently_compared(self):
        run, expected = self.run_input()
        run['suite_sha256'] = 'different-suite'
        with self.assertRaises(ValueError):
            self.evaluate(run, expected)

    def test_case_and_safety_evidence_required(self):
        for target in ('case', 'safety'):
            run, expected = self.run_input()
            (run['cases'][0] if target == 'case' else run['safety']['privacy'])['evidence'] = ''
            with self.subTest(target=target), self.assertRaises(ValueError):
                self.evaluate(run, expected)

    def test_unsuccessful_bootstrap_is_quality_review(self):
        run, expected = self.run_input()
        run['bootstrap'] = 'FAIL'
        self.assertEqual(self.evaluate(run, expected)['verdict'], 'REVIEW')


if __name__ == '__main__':
    unittest.main()
