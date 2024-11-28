# config_translator/utils.py
import re
from math import pow

def evaluate_constant_expression(expression):
    """
    Вычисляет значение выражения в постфиксной нотации.
    Поддерживает операции: +, -, pow(), len(), /.
    """
    # Убираем обрамляющие ".{" и "}."
    if expression.startswith(".{") and expression.endswith("}."):
        expression = expression[2:-2].strip()
    else:
        raise ValueError("Expression must be enclosed in '.{' and '}.'")

    # Определяем регулярное выражение для токенов
    tokens = re.findall(r'len\(\s*\[.*?\]\s*\)|[^\s]+', expression)  # Находит все вызовы len() и другие токены

    stack = []

    for token in tokens:
        if token.isdigit():  # Число
            stack.append(int(token))
        elif token == "+":  # Сложение
            b = stack.pop()
            a = stack.pop()
            stack.append(a + b)
        elif token == "-":  # Вычитание
            b = stack.pop()
            a = stack.pop()
            stack.append(a - b)
        elif token == "/":  # Деление
            b = stack.pop()
            a = stack.pop()
            if b == 0:
                raise ValueError("Division by zero")
            stack.append(a / b)
        elif token == "pow()":  # Степень
            b = stack.pop()
            a = stack.pop()
            stack.append(pow(a, b))
        elif token.startswith("len(") and token.endswith(")"):  # Обработка len() для массивов
            # Извлекаем содержимое массива
            array_content = token[4:-1].strip()  # Убираем "len(" и ")"

            # Удаляем пробелы и разбиваем на элементы
            elements = re.findall(r"'([^']+)'|([^\s,;]+)", array_content)
            elements = [e[0] or e[1] for e in elements if e[0] or e[1]]  # Фильтрация пустых элементов
            stack.append(len(elements)-2)
        else:
            raise ValueError(f"Unsupported operation or token: {token}")

    if len(stack) != 1:
        raise ValueError("Invalid expression")
    return stack.pop()
