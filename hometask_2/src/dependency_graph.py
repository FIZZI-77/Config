import subprocess
import json
import os


def get_npm_dependencies(package_name):
    """
    Возвращает зависимости указанного npm-пакета.
    """
    cmd = ['npm', 'view', package_name, 'dependencies', '--json']
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception(f"Ошибка получения зависимостей для пакета {package_name}.")
    return json.loads(result.stdout) if result.stdout else {}


def save_dependencies_to_file(package_name, dependencies, file_path="data/package_dependencies.json"):
    """
    Сохраняет зависимости в файл JSON.
    """
    data = {"packageName": package_name, "dependencies": dependencies}
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def load_dependencies_from_file(package_name, file_path="data/package_dependencies.json"):
    """
    Загружает зависимости из файла JSON.
    """
    if not os.path.exists(file_path):
        return None

    with open(file_path, "r") as f:
        data = json.load(f)
        if data.get("packageName") == package_name:
            return data["dependencies"]
    return None


def build_dependency_graph(package_name, visited=None):
    """
    Рекурсивно строит граф зависимостей.
    """
    if visited is None:
        visited = {}

    # Проверяем, есть ли данные в кеше
    cached_dependencies = load_dependencies_from_file(package_name)
    if cached_dependencies:
        visited[package_name] = list(cached_dependencies.keys())
        return visited

    # Получаем зависимости через npm
    dependencies = get_npm_dependencies(package_name)
    visited[package_name] = list(dependencies.keys())

    for dep in dependencies.keys():
        if dep not in visited:
            build_dependency_graph(dep, visited)

    # Сохраняем результаты
    save_dependencies_to_file(package_name, dependencies)
    return visited

def flatten_dependencies(package_name, dependencies, graph=None):
    """
    Преобразует вложенные зависимости в плоский граф.
    """
    if graph is None:
        graph = {}

    if package_name not in graph:
        graph[package_name] = []

    for dep, subdeps in dependencies.items():
        graph[package_name].append(dep)
        flatten_dependencies(dep, subdeps, graph)

    return graph
