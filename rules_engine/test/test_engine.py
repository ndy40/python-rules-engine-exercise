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
        dict_rule = {"and": {"temperature": {"is above": 10}, "age": {"is above": 10}}}
        input_data = {"temperature": 15, "age": 11}
        self.assertTrue(evaluate(dict_rule, input_data))

    def test_rule_engine_succeeds_with_combination_clause_of_and_with_or_groupings(
        self,
    ):
        dict_rule = {
            "and": {"temperature": {"is above": 10}, "age": {"is above": 10}},
            "or": {"name": {"equals": "john"}},
        }
        input_data = {"temperature": 15, "age": 11, "name": "john"}
        self.assertTrue(evaluate(dict_rule, input_data))

    def test_rules_can_be_created_using_grouping_clause_with_non_grouping_clause(self):
        dict_rule = {
            "and": {"temperature": {"is above": 10}, "age": {"is above": 10}},
            "name": {"equals": "john"},
        }
        input_data = {"temperature": 15, "age": 11, "name": "john"}
        self.assertTrue(evaluate(dict_rule, input_data))

    def test_rules_fails_grouping_clause_with_non_grouping_clause(self):
        dict_rule = {
            "and": {"temperature": {"is above": 20}, "age": {"is above": 10}},
            "name": {"equals": "john"},
        }
        input_data = {"temperature": 15, "age": 11, "name": "Not john"}
        self.assertFalse(evaluate(dict_rule, input_data))

    def test_rules_evaluate_to_true_using_and_or_combination_clause_in_rule_definition(
        self,
    ):
        dict_rule = {
            "and": {"temperature": {"is above": 20}, "age": {"is above": 10}},
            "or": {"name": {"equals": "john"}},
        }
        input_data = {"temperature": 15, "age": 11, "name": "Not john"}
        self.assertFalse(evaluate(dict_rule, input_data))