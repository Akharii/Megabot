# -*- coding: utf-8 -*-

import random
from textx import metamodel_from_str


grammar = """
RollCommand:
    'roll' expr=DiceExpr 
;

DiceExpr: 
    (expr=FunctionCall | expr=Dice) (op=Operator value=/[0-9]+/)?
;

FunctionCall:
    name=FunctionName '(' params*=DiceExpr ')'
;

FunctionName:
    "sort" | "sum" | "max" | "min"
;

Dice:
    num=/[0-9]+/'d'dice=/[0-9]+/
;

Operator: 
    '+' | '-'
;
"""

metamodel = metamodel_from_str(grammar)


def compute_roll_value(model):
    return __eval_expr(model.expr)


def __eval_expr(expr):
    match expr.__class__.__name__:
        case "DiceExpr":
            result = __eval_expr(expr.expr)
            if expr.op == "+":
                result = [e + int(expr.value) for e in result]
            elif expr.op == "-":
                result = [e - int(expr.value) for e in result]
            return result
        case "Dice":
            result = []
            for _ in range(int(expr.num)):
                result.append(random.randint(1, int(expr.dice)))
            return result
        case "FunctionCall":
            params = []
            for p in expr.params:
                params += __eval_expr(p)
            if expr.name == "sum":
                return [sum(params)]
            elif expr.name == "sort":
                return sorted(params)
            elif expr.name == "max":
                return [max(params)]
            elif expr.name == "min":
                return [min(params)]
        case _:
            print(dir(expr))


def __test(command):
    print(f"TEST {command}")
    test = metamodel.model_from_str(command)
    print(compute_roll_value(test))


if __name__ == "__main__":
    __test("roll 2d6")
    __test("roll 2d6+2")
    __test("roll sort(12d6)+2")
    __test("roll sum(2d6 4d4)")
    __test("roll sort(sum(2d6) max(2d5)+2)-1")
