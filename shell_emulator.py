import zipfile
import os
import json  # Импортируем библиотеку json
import shutil
import tkinter as tk
from tkinter import scrolledtext, messagebox


class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.cwd = '/'  # Текущая рабочая директория
        self.history = []  # История команд
        self.output = []  # Список для хранения вывода
        self.load_virtual_fs()  # Загрузка виртуальной файловой системы
        self.current_directory = "/"

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)  # Загрузка конфигурации из JSON
            self.computer_name = config['computer']['name']
            self.zip_path = config['filesystem']['path']
            self.startup_script = config['startup']['script']

    def load_virtual_fs(self):
        self.zip_file = zipfile.ZipFile(self.zip_path, 'r')
        self.files = list(set(self.zip_file.namelist()))

    def initialize(self):
        self.run_startup_script()  # Запуск стартового скрипта после инициализации GUI

    def run_startup_script(self):
        try:
            with self.zip_file.open(self.startup_script) as f:
                for line in f:
                    command = line.decode('utf-8').strip()
                    if command:
                        self.execute_command(command)
        except KeyError:
            self.show_output(f"Startup script '{self.startup_script}' not found in zip file.")

    def execute_command(self, command):
        self.history.append(command)
        parts = command.split()

        if parts[0] == 'ls':
            self.ls()
        elif parts[0] == 'cd':
            self.cd(parts[1] if len(parts) > 1 else '.')
        elif parts[0] == 'exit':
            self.exit_shell()
        elif parts[0] == 'rm':
            if len(parts) > 1:
                self.rm(parts[1])
            else:
                self.show_output("Usage: rm <file>")
        elif parts[0] == 'rmdir':
            if len(parts) > 1:
                self.rmdir(parts[1])
            else:
                self.show_output("Usage: rmdir <directory>")
        elif parts[0] == 'history':
            self.show_history()
        else:
            self.show_output(f"Command '{parts[0]}' not found")

    def ls(self):
        if self.cwd == '/':
            cwd_with_slash = ''
        else:
            cwd_with_slash = self.cwd.rstrip('/') + '/'

        items = set()
        for file in self.files:
            if file.startswith(cwd_with_slash) and file != cwd_with_slash:
                relative_path = file[len(cwd_with_slash):].strip('/')
                if '/' in relative_path:
                    directory = relative_path.split('/')[0]
                    items.add(directory + '/')
                else:
                    items.add(relative_path)

        if items:
            self.show_output("\n".join(sorted(items)))
        else:
            self.show_output("Directory is empty")

    def cd(self, path):
        if path == '..':
            self.cwd = os.path.dirname(self.cwd.rstrip('/'))
            if not self.cwd:
                self.cwd = '/'
        else:
            new_path = os.path.join(self.cwd.rstrip('/'), path).replace('\\', '/').lstrip('/')
            if any(file.startswith(new_path + '/') or file == new_path for file in self.files):
                self.cwd = new_path
                self.show_output(f"Changed directory to {self.cwd}")
            else:
                self.show_output(f"Directory '{path}' not found")
        print(f"DEBUG: cwd={self.cwd}, path={path}")  # Отладка



    def rm(self, path):
        # Приводим путь к универсальному формату
        full_path = os.path.join(self.cwd.rstrip('/'), path).replace('\\', '/').lstrip('/')
        print(f"DEBUG: cwd={self.cwd}, full_path={full_path}, files={self.files}")  # Отладка
        

        # Проверяем, что это не директория
        if full_path.endswith('/'):
            self.show_output(f"'{full_path}' is a directory. Use 'rmdir' to remove directories.")
            return

        # Проверяем, существует ли файл
        if full_path in self.files:
            self.files = [f for f in self.files if f != full_path]  # Удаляем файл
            self.show_output(f"Removed file '{full_path}'")
            print(f"DEBUG after rm: files={self.files}")  # Проверка после удаления
        else:
            self.show_output(f"File '{full_path}' not found")


    def rmdir(self, path):
        full_path = os.path.join(self.cwd.rstrip('/'), path).rstrip('/') + '/'
        if any(file.startswith(full_path) for file in self.files):
            self.files = [f for f in self.files if not f.startswith(full_path)]
            self.show_output(f"Removed directory {full_path} (virtual removal)")
        else:
            self.show_output(f"Directory '{path}' not found")


    def show_history(self):
        self.show_output("\n".join(self.history))

    def exit_shell(self):
        self.show_output("Exiting shell...")
        exit()

    def show_output(self, output):
        self.output.append(output)
        if hasattr(self, 'output_area'):
            self.output_area.configure(state='normal')
            self.output_area.insert(tk.END, output + "\n")
            self.output_area.configure(state='disabled')
            self.output_area.see(tk.END)  # Прокрутка к последнему выводу

    def get_output(self):
        return "\n".join(self.output)

    def clear_output(self):
        self.output = []

    def execute_gui_command(self):
        command = self.input_area.get()
        self.input_area.delete(0, tk.END)
        if command.strip().lower() == "exit":
            self.exit_shell()
        else:
            self.execute_command(command)


def main():
    # Создание главного окна
    root = tk.Tk()
    root.title("Shell Emulator")

    shell = ShellEmulator('config.json')  # Запускаем эмулятор с заданным конфигурационным файлом

    # Настройка области вывода
    shell.output_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, state='disabled', height=20, width=50)
    shell.output_area.pack(padx=10, pady=10)

    # Настройка поля ввода
    shell.input_area = tk.Entry(root, width=50)
    shell.input_area.pack(padx=10, pady=10)
    shell.input_area.bind('<Return>', lambda event: shell.execute_gui_command())  # Вызов команды по нажатию Enter

    shell.initialize()  # Запуск стартового скрипта после создания GUI

    root.mainloop()  # Запуск GUI


if __name__ == '__main__':
    main()