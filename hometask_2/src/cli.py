import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description="Визуализатор графа зависимостей npm-пакета.")
    parser.add_argument("--package-name", required=True, help="Имя анализируемого npm-пакета.")
    return parser.parse_args()
