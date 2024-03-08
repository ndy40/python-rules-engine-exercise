from rules_engine.models import Rule

AND_RULES_CLAUSE = "and"
OR_RULES_CLAUSE = "or"

SUPPORTED_RULES_CLAUSE = [AND_RULES_CLAUSE, OR_RULES_CLAUSE]


def _combine_rules(ops, left_rule, right_rule):
    if left_rule is None:
        left_rule = right_rule

    match ops:
        case "and":
            left_rule = left_rule & right_rule
        case "or":
            left_rule = left_rule | right_rule
    return left_rule


def _derive_operator_and_condition(variable, condition) -> tuple[str, dict]:
    if isinstance(condition, dict):
        op, *_ = condition
    else:
        op = variable
        condition = {variable: condition}
    return (
        op,
        condition,
    )


def _build_rule_from_dict(ops_clause, data):
    tmp = None
    for variable, condition in data.items():
        operator, condition = _derive_operator_and_condition(variable, condition)

        if operator not in SUPPORTED_RULES_CLAUSE:
            # most likely a variable, so we force an "and" combination.
            ops_clause = AND_RULES_CLAUSE

            # Extract operator from structure {'operator': value} or {'variable': {'operatore': value}}
            operator, expr = next(iter(condition.items()))

            # TODO: Refactor to remove nested if statements.
            if isinstance(expr, dict):
                operator, value = next(iter(expr.items()))
            else:
                value = expr
        else:
            value = condition[operator]

        current_rule = Rule(variable=variable, op=operator, value=value)

        tmp = (
            _combine_rules(ops_clause, tmp, current_rule)
            if tmp is not None
            else current_rule
        )
    return tmp


def _parse_rule(condition: dict):
    for ops in condition.keys():
        rule = condition[ops]
        if ops not in SUPPORTED_RULES_CLAUSE:
            ops = None
            rule = condition
        yield _build_rule_from_dict(ops, rule)


def evaluate(rules: dict, data: dict):
    eval_rule = [rule.evaluate(data) for rule in _parse_rule(rules)]
    return any(eval_rule)
