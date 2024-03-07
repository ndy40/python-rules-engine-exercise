from unittest import TestCase

from rules_engine.engine import evaluate


class RuleEngineTests(TestCase):

    def test_rule_engine_evals_to_true(self):
        dict_rule = {"temperature": {"is above": 10}}
        input_data = {"temperature": 15}
        self.assertTrue(evaluate(dict_rule, input_data))