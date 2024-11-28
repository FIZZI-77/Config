import yaml
from .parser import validate_yaml_structure, parse_yaml_to_uya
from .constants import evaluate_constant_expression  # Импортируем функцию для вычислений

def translate(input_path, output_path):
    # Чтение YAML-файла
    with open(input_path, "r") as file:
        yaml_data = yaml.safe_load(file)

    # Валидация структуры
    validate_yaml_structure(yaml_data)

    # Преобразование в УЯ
    uya_output = parse_yaml_to_uya(yaml_data)

    # Запись результата в файл
    with open(output_path, "w") as file:
        file.write(uya_output)
