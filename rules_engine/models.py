import abc

OPERATOR_FUNC_MAPPINGS = {
    "is above": lambda data_value, rule_value: data_value > rule_value,
    "is below": lambda data_value, rule_value: data_value < rule_value,
}


class AbstractRule(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, data): ...

    def __and__(self, other):
        return AndRule(self, other)

    def __or__(self, other):
        return OrRule(self, other)


class Rule(AbstractRule):
    def __init__(self, variable: str, op: str, value: str):
        self.variable = variable
        self.op = op.lower()
        self.value = value

    def evaluate(self, data):
        if self.op not in OPERATOR_FUNC_MAPPINGS:
            raise ValueError("operator not supported")

        if data_value := data.get(self.variable):
            return OPERATOR_FUNC_MAPPINGS[self.op](data_value, self.value)

        return False


class AndRule(AbstractRule):
    def __init__(self, first: AbstractRule, second: AbstractRule):
        self.first = first
        self.second = second

    def evaluate(self, data):
        return self.first.evaluate(data) and self.second.evaluate(data)


class OrRule(AbstractRule):
    def __init__(self, first: AbstractRule, second: AbstractRule):
        self.first = first
        self.second = second

    def evaluate(self, data):
        return self.first.evaluate(data) or self.second.evaluate(data)