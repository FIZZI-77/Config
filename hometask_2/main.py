from src.cli import parse_arguments
from src.dependency_graph import build_dependency_graph
from src.plantuml_generator import generate_plantuml_content

def main():
    args = parse_arguments()

    # Построение графа зависимостей
    print(f"Получение зависимостей для пакета: {args.package_name}")
    dependency_graph = build_dependency_graph(args.package_name)

    # Генерация PlantUML-контента
    print("Генерация PlantUML-графа...")
    plantuml_content = generate_plantuml_content(dependency_graph)

    # Сохранение PlantUML-файла
    with open("graph.puml", "w") as f:
        f.write(plantuml_content)

    print("Граф зависимостей успешно построен.")
    print("Откройте файл `graph.puml` в VS Code для визуализации.")


if __name__ == "__main__":
    main()
