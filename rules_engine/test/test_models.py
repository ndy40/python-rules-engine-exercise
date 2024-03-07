from unittest import TestCase

from rules_engine.models import Rule


class RuleModelTest(TestCase):
    def test_rule_evaluate_above_true(self):
        rule = Rule("temperature", "is above", 30)
        data = {"temperature": 35}
        self.assertTrue(rule.evaluate(data))

    def test_rule_evaluate_above_false(self):
        rule = Rule("temperature", "is above", 30)
        data = {"temperature": 25}
        self.assertFalse(rule.evaluate(data))

    def test_rule_evaluate_below_true(self):
        rule = Rule("temperature", "is below", 30)
        data = {"temperature": 25}
        self.assertTrue(rule.evaluate(data))

    def test_rule_evaluate_below_false(self):
        rule = Rule("temperature", "is below", 30)
        data = {"temperature": 35}
        self.assertFalse(rule.evaluate(data))

    def test_rule_evaluate_unsupported_operator(self):
        rule = Rule("temperature", "greater than but equals", 30)
        data = {"temperature": 30}
        with self.assertRaises(ValueError):
            rule.evaluate(data)

    def test_and_rule_evaluate_true(self):
        first_rule = Rule("temperature", "is above", 20)
        second_rule = Rule("pressure", "is below", 100)
        and_rule = first_rule & second_rule
        data = {"temperature": 25, "pressure": 90}
        self.assertTrue(and_rule.evaluate(data))

    def test_and_rule_evaluate_false(self):
        first_rule = Rule("temperature", "is above", 20)
        second_rule = Rule("pressure", "is below", 100)
        and_rule = first_rule & second_rule
        data = {"temperature": 15, "pressure": 90}
        self.assertFalse(and_rule.evaluate(data))

    def test_or_rule_evaluate_true(self):
        first_rule = Rule("temperature", "is above", 20)
        second_rule = Rule("pressure", "is below", 100)
        or_rule = first_rule | second_rule
        data = {"temperature": 15, "pressure": 90}
        self.assertTrue(or_rule.evaluate(data))

    def test_or_rule_evaluate_false(self):
        first_rule = Rule("temperature", "is above", 20)
        second_rule = Rule("pressure", "is below", 100)
        or_rule = first_rule | second_rule
        data = {"temperature": 15, "pressure": 110}
        self.assertFalse(or_rule.evaluate(data))