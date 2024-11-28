from .constants import evaluate_constant_expression  # Импортируем функцию вычислений

def validate_yaml_structure(data):
    print(f"Validating structure: {data}")
    if not isinstance(data, dict):
        raise ValueError("Top-level structure must be a dictionary.")



def parse_yaml_to_uya(data):
    def process_value(value):
        if isinstance(value, dict):
            return "begin\n" + "".join(
                f" {key} := {process_value(val)};\n" for key, val in value.items()
            ) + "end"
        elif isinstance(value, list):
            return "[ " + "; ".join(map(process_value, value)) + " ]"
        elif isinstance(value, str):
            return f"'{value}'"
        elif isinstance(value, (int, float)):
            return str(value)
        else:
            raise ValueError(f"Unsupported value type: {type(value)}")

    result = []
    for key, value in data.items():
        if isinstance(value, str) and value.startswith(".{") and value.endswith("}."):
            # Используем evaluate_constant_expression для вычислений
            try:
                const_value = evaluate_constant_expression(value)
                result.append(f"var {key} {const_value};")
            except Exception as e:
                print(f"Error evaluating expression for key {key}: {e}")
                raise  # Пробрасываем исключение, чтобы остановить выполнение
        else:
            result.append(f"var {key} {process_value(value)};")
    return "\n".join(result)
