from unittest import TestCase

from rules_engine.engine import evaluate


class RuleEngineTests(TestCase):

    def test_rule_engine_evals_to_true(self):
        dict_rule = {"temperature": {"is above": 10}}
        input_data = {"temperature": 15}
        self.assertTrue(evaluate(dict_rule, input_data))

    def test_rule_engine_evals_to_false(self):
        dict_rule = {"temperature": {"is above": 10}}
        input_data = {"temperature": 15}
        self.assertTrue(evaluate(dict_rule, input_data))

    def test_rule_engine_works_without_combination_clause_groupings(self):
        dict_rule = {"temperature": {"is above": 10}, "age": {"is above": 10}}
        input_data = {"temperature": 15, "age": 11}
        self.assertTrue(evaluate(dict_rule, input_data))

    def test_rule_engine_succeeds_with_combination_clause_groupings(self):
        dict_rule = {'and': {"temperature": {"is above": 10}, "age": {"is above": 10}}}
        input_data = {"temperature": 15, "age": 11}
        self.assertTrue(evaluate(dict_rule, input_data))