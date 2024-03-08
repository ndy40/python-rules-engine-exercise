from rules_engine.models import Rule


dict_rule = {
    "and": {"credit_rating": {"is above": 50}, "flood_risk": {"is below": 10}},
    "or": {"revenue": {"is above": 900}, "flood_risk": {"is below": 10}},
}

SUPPORTED_RULES_CLAUSE = ["and", "or"]


def _eval_rule(ops, rule1, rule2):
    if rule1 is None:
        rule1 = rule2

    match ops:
        case "and":
            rule1 = rule1 & rule2
        case "or":
            rule1 = rule1 | rule2
    return rule1


def _build_rule_from_dict(ops_clause, data):
    tmp = None
    for variable, condition in data.items():
        if isinstance(condition, dict):
            op, *_ = condition
        else:
            op = variable
            condition = {variable: condition}

        # create rule from op
        if op not in SUPPORTED_RULES_CLAUSE:
            ops_clause = "and"

            _, expr = next(iter(condition.items()))
            if isinstance(expr, dict):
                op, value = next(iter(expr.items()))
            else:
                op, value = (_, expr)
        else:
            value = condition[op]
        current_rule = Rule(variable=variable, op=op, value=value)
        tmp = (
            _eval_rule(ops_clause, tmp, current_rule)
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
