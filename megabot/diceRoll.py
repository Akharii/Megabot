import random
import re

class DiceRoll:
    def __init__(self, num_dice, num_sides):
        self.num_dice = num_dice
        self.num_sides = num_sides

    def roll(self):
        return [random.randint(1, self.num_sides) for _ in range(self.num_dice)]

def evaluate_dice_expression(expression):
    #recherche des tokens avec regex
    tokens = re.findall(r'\d+|d|\w+|[()+*-]', expression)

    #construction d'un arbre'
    tree = parse_expression(tokens)

    # Évaluation de l'arbre
    result = evaluate_tree(tree)
    return result

#on construit l'rabre
def parse_expression(tokens):
    tree = []
    i = 0

    while i < len(tokens):
        token = tokens[i]

        if token.isdigit():  # Nombre de dés
            if i + 1 < len(tokens) and tokens[i + 1] == 'd':
                num_dice = int(token)
                num_sides = int(tokens[i + 2])
                dice_roll = DiceRoll(num_dice, num_sides)
                tree.append(dice_roll)
                i += 2
            else:
                raise ValueError("Erreur de syntaxe")

        elif token == 'sum' or token == 'max' or token == 'sort':  # Fonction
            if i + 1 < len(tokens) and tokens[i + 1] == '(':
                j = i + 2
                count = 1
                while count > 0 and j < len(tokens):
                    if tokens[j] == '(':
                        count += 1
                    elif tokens[j] == ')':
                        count -= 1
                    j += 1

                if count != 0:
                    raise ValueError("Erreur de syntaxe")

                subexpression = tokens[i + 2:j - 1]
                sub_tree = parse_expression(subexpression)
                tree.append((token, sub_tree))
                i = j - 1
            else:
                raise ValueError("Erreur de syntaxe")

        elif token in ['+', '-', '*', '/']:  # Opérateur
            tree.append(token)

        i += 1

    return tree

def evaluate_tree(tree):
    if isinstance(tree, list):
        if len(tree) == 1:
            return evaluate_tree(tree[0])

        result = evaluate_tree(tree[0])
        for i in range(1, len(tree), 2):
            operator = tree[i]
            operand = evaluate_tree(tree[i + 1])

            if operator == '+':
                result += operand
            elif operator == '-':
                result -= operand
            elif operator == '*':
                result *= operand
            elif operator == '/':
                result /= operand
            else:
                raise ValueError("Opérateur invalide")

        return result

    elif isinstance(tree, DiceRoll):
        return tree.roll()

    elif isinstance(tree, tuple):
        function = tree[0]
        sub_tree = tree[1]

        if function == 'sum':
            rolls = evaluate_tree(sub_tree)
            return sum(rolls)
        elif function == 'max':
            rolls = evaluate_tree(sub_tree)
            return max(rolls)
        elif function == 'sort':
            rolls = evaluate_tree(sub_tree)
            rolls.sort()
            return rolls
        else:
            raise ValueError("Fonction invalide")

    else:
        raise ValueError("Arbre invalide")
