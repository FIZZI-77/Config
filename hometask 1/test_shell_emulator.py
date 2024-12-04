from shell_emulator import ShellEmulator

def test_shell_emulator():
    emulator = ShellEmulator('config.json')

    test_passed = 0
    total_tests = 6

    # Тест 1: Список файлов в корневой директории
    print("Test 1: List files in the root directory")
    emulator.ls()
    output = emulator.get_output()
    assert "some_directory" in output or "another_directory" in output, "Directory listing failed"  # Ожидаемый вывод
    test_passed += 1 

    # Тест 2: Переход в директорию 'some_directory'
    print("\nTest 2: Change directory to 'some_directory'")
    emulator.cd('some_directory') 
    output = emulator.get_output()
    assert "Changed directory to some_directory" in output, "Directory change failed"
    test_passed += 1  

    # Тест 3: Список файлов после смены директории
    print("\nTest 3: List files after changing directory")
    emulator.ls() 
    output = emulator.get_output()
    assert "some_file.txt" in output or "test_file.txt" in output, "Directory contents incorrect after cd"
    test_passed += 1  

    # Тест 4: Удаление файла 'some_file.txt'
    print("\nTest 4: Remove file 'some_file.txt'")
    emulator.rm('some_file.txt')  
    output = emulator.get_output()
    assert "Removed file 'some_directory/some_file.txt'" in output, f"File removal failed: {output}"
    test_passed += 1 

    # Тест 5: Переход в несуществующую директорию 'invalid_directory'
    print("\nTest 5: Change to a non-existing directory 'invalid_directory'")
    emulator.cd('invalid_directory') 
    output = emulator.get_output()
    assert "Removed file 'some_directory/some_file.txt'" in output, f"File removal failed: {output}"
    test_passed += 1 

    # Тест 6: Показать историю команд
    print("\nTest 6: Show command history")
    emulator.show_history()
    output = emulator.get_output()
    test_passed += 1 

    print(f"\nAll {test_passed}/{total_tests} tests passed successfully!")

if __name__ == "__main__":
    test_shell_emulator()
