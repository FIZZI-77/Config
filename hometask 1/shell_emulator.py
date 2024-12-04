import zipfile
import os
import json  # Импортируем библиотеку json
import tkinter as tk
from tkinter import scrolledtext, messagebox


class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.cwd = '/'  # Текущая рабочая директория
        self.history = []  # История команд
        self.output = []  # Список для хранения вывода
        self.load_virtual_fs()  # Загрузка виртуальной файловой системы из zip
        self.current_directory = "/"
        self.log_actions = []  # Лог действий

    def load_config(self, config_path):
        with open(config_path, 'r') as f:
            config = json.load(f)
            self.computer_name = config['computer']['name']
            self.zip_path = config['filesystem']['path']
            self.startup_script = config['startup']['script']
            self.log_path = config['logging']['path']  # Путь к лог-файлу

    def log_action(self, action_type, details):
        """Добавить действие в лог."""
        action = {
            "type": action_type,
            "details": details,
            "cwd": self.cwd
        }
        self.log_actions.append(action)

        # Сохранить логи в JSON файл
        with open(self.log_path, 'w') as log_file:
            json.dump(self.log_actions, log_file, indent=4)

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
        self.log_action("execute_command", {"command": command})
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
        elif parts[0] == 'clear':
            self.clear_output()  # Очистить вывод
            self.show_output("Screen cleared.")
        elif parts[0] == 'cp':
            if len(parts) > 2:
                self.cp(parts[1], parts[2])  # Копирование файла
            else:
                self.show_output("Usage: cp <source> <destination>")
        elif parts[0] == 'head':
            if len(parts) > 1:
                self.head(parts[1])  # Показать первые строки файла
            else:
                self.show_output("Usage: head <file>")
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
        self.log_action("ls", {"cwd": self.cwd})

    def cd(self, path):
        previous_cwd = self.cwd
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
        self.log_action("cd", {"from": previous_cwd, "to": self.cwd})

    def rm(self, path):
        full_path = os.path.join(self.cwd.rstrip('/'), path).replace('\\', '/').lstrip('/')
        if full_path.endswith('/'):
            self.show_output(f"'{full_path}' is a directory. Use 'rmdir' to remove directories.")
            return

        if full_path in self.files:
            self.files = [f for f in self.files if f != full_path]
            self.show_output(f"Removed file '{full_path}'")
        else:
            self.show_output(f"File '{full_path}' not found")
        self.log_action("rm", {"file": path})

    def rmdir(self, path):
        full_path = os.path.join(self.cwd.rstrip('/'), path).rstrip('/') + '/'
        if any(file.startswith(full_path) for file in self.files):
            self.files = [f for f in self.files if not f.startswith(full_path)]
            self.show_output(f"Removed directory {full_path} (virtual removal)")
        else:
            self.show_output(f"Directory '{path}' not found")
        self.log_action("rmdir", {"directory": path})

    def show_history(self):
        self.show_output("\n".join(self.history))
        self.log_action("show_history", {"history": self.history})

    def exit_shell(self):
        self.show_output("Exiting shell...")
        self.log_action("exit_shell", {})
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

    def head(self, file_path):
        """Показать первые несколько строк файла."""
        file_path = os.path.join(self.cwd.rstrip('/'), file_path).replace('\\', '/').lstrip('/')
        if file_path in self.files:
            with self.zip_file.open(file_path) as f:
                lines = f.readlines()
                for i in range(min(10, len(lines))):  # Показать первые 10 строк
                    self.show_output(lines[i].decode('utf-8').strip())
        else:
            self.show_output(f"File '{file_path}' not found")

        self.log_action("head", {"file": file_path})

    def cp(self, source, destination):
        """Копировать файл из source в destination."""
        source = os.path.join(self.cwd.rstrip('/'), source).replace('\\', '/').lstrip('/')
        destination = os.path.join(self.cwd.rstrip('/'), destination).replace('\\', '/').lstrip('/')

        if source in self.files:
            # Проверим, если файл уже существует в назначении
            if destination not in self.files:
                self.files.append(destination)
                self.show_output(f"File '{source}' copied to '{destination}'")
            else:
                self.show_output(f"Destination file '{destination}' already exists")
        else:
            self.show_output(f"Source file '{source}' not found")

        self.log_action("cp", {"source": source, "destination": destination})

    def clear_output(self):
        self.output = []  # Очищаем вывод
        if hasattr(self, 'output_area'):
            self.output_area.configure(state='normal')
            self.output_area.delete(1.0, tk.END)
            self.output_area.configure(state='disabled')
            self.show_output("Output cleared.")  # Показать сообщение о том, что вывод очищен.

    def execute_gui_command(self):
        command = self.input_area.get().strip()  # Убираем пробелы по краям
        self.input_area.delete(0, tk.END)  # Очищаем поле ввода

        if command == "":  # Игнорируем пустую строку
            return  # Просто выходим из метода без вывода ошибок

        if command.lower() == "exit":
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

    # Настройка поля для ввода команды
    shell.input_area = tk.Entry(root, width=50)
    shell.input_area.pack(padx=10, pady=10)
    shell.input_area.bind("<Return>", lambda event: shell.execute_gui_command())  # Ввод команды по нажатию Enter

    shell.initialize()  # Инициализация эмулятора после загрузки всех компонентов

    # Запуск приложения
    root.mainloop()


if __name__ == '__main__':
    main()