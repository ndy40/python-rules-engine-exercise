import abc

OPERATOR_FUNC_MAPPINGS = {
    "is above": lambda data_value, rule_value: data_value > rule_value,
    "is below": lambda data_value, rule_value: data_value < rule_value,
    "equals": lambda data_value, rule_value: data_value == rule_value,
    "not equals": lambda data_value, rule_value: data_value != rule_value,
    "at most": lambda data_value, rule_value: data_value >= rule_value,
    "at least": lambda data_value, rule_value: data_value <= rule_value,
}


class AbstractRule(abc.ABC):
    @abc.abstractmethod
    def evaluate(self, data): ...

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def __and__(self, other):
        return _AndRule(self, other)

    def __or__(self, other):
        return _OrRule(self, other)


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

    def __repr__(self):
        return f"{self.__class__.__name__}({self.variable}, {self.op}, {self.value})"


class _AndRule(AbstractRule):
    def __init__(self, first: AbstractRule, second: AbstractRule):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"{self.__class__.__name__}({self.first}, {self.second})"

    def evaluate(self, data):
        return self.first.evaluate(data) and self.second.evaluate(data)


class _OrRule(AbstractRule):
    def __init__(self, first: AbstractRule, second: AbstractRule):
        self.first = first
        self.second = second

    def __repr__(self):
        return f"{self.__class__.__name__}({self.first}, {self.second})"

    def evaluate(self, data):
        return self.first.evaluate(data) or self.second.evaluate(data)