import os
import subprocess

def generate_plantuml_content(graph):
    """
    Генерирует текстовое представление графа для PlantUML.
    """
    lines = ["@startuml"]
    for package, deps in graph.items():
        for dep in deps:
            lines.append(f'"{package}" --> "{dep}"')
    lines.append("@enduml")
    return "\n".join(lines)


def generate_graph_image(plantuml_content, visualizer_path):
    """
    Генерирует изображение графа с помощью PlantUML.
    """
    with open("graph.puml", "w") as f:
        f.write(plantuml_content)

    cmd = ["java", "-jar", visualizer_path, "graph.puml"]
    subprocess.run(cmd, check=True)

    if not os.path.exists("graph.png"):
        raise Exception("Ошибка генерации изображения графа.")
