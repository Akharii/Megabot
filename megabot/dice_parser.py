# -*- coding: utf-8 -*-

import random
from textx import metamodel_from_str


__metamodel = metamodel_from_str(
    """
RollCommand:
    'roll' expr=DiceExpr (cop=ConditionalOperator value=/[0-9]+/)? 
;

DiceExpr: 
    (expr=FunctionCall | expr=Dice) (op=Operator value=/[0-9]+/)?
;

FunctionCall:
    name=FunctionName '(' params+=DiceExpr ')'
;

FunctionName:
    "sort" | "sum" | "max" | "min"
;

Dice:
    num=/[0-9]+/'d'dice=/[0-9]+/
;

Operator: 
    '+' | '-' | '*' | '/' | 'mod'
;

ConditionalOperator:
    '<' | '>' | '>=' | '<='
;
"""
)


def compute_roll_value(roll: str) -> list[int]:
    return __eval_expr(__metamodel.model_from_str(roll))


def __eval_expr(expr):
    #print(f" math: {expr.__class__.__name__}")
    match expr.__class__.__name__:
        case "DiceExpr":
            result = __eval_expr(expr.expr)
            if expr.op == "+":
                result = [e + int(expr.value) for e in result]
            elif expr.op == "-":
                result = [e - int(expr.value) for e in result]
            elif expr.op == "*":
                result = [e * int(expr.value) for e in result]
            elif expr.op == "/":
                result = [e / int(expr.value) for e in result]
            elif expr.op == "mod":
                result = [e % int(expr.value) for e in result]
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

        case "RollCommand":
            result = __eval_expr(expr.expr)
            if expr.cop == "<":
                [e for e in result if e < int(expr.value)]
            elif expr.cop == ">":
                result = [e for e in result if e > int(expr.value)]
            elif expr.cop == "<=":
                result = [e for e in result if e <= int(expr.value)]
            elif expr.cop == ">=":
                result = [e for e in result if e >= int(expr.value)]
            return result

if __name__ == "__main__":

    def __test(command):
        print(f"TEST {command}")
        print(compute_roll_value(command))

    __test("roll 2d6")
    __test("roll 2d6+2")
    __test("roll sort(12d6)+2")
    __test("roll sum(2d6 4d4)")
    __test("roll sort(sum(2d6) max(2d5)+2)-1")
    __test("roll 3d")
