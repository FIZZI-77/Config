# Конвертер конфигурации

## Общее описание
Этот проект реализует конвертер, который преобразует YAML-конфигурационные файлы в учебный конфигурационный язык (UYA). Он позволяет пользователям описывать переменные, массивы и константы в формате YAML, который затем преобразуется в формат, предназначенный для образовательных целей.

## Структура файлов
Проект состоит из следующих файлов:

- **config_translator/parser.py**: Содержит основные функции для парсинга YAML и преобразования в формат UYA.
- **config_translator/constants.py**: Реализует логику для вычисления выражений и выполнения операций с массивами и переменными.
- **config_translator/tests.py**: Содержит тесты для проверки корректности конвертации и обработки данных.
- **library_config.yml**: Пример входного YAML-файла для тестирования конвертера.
- **output_data/example_output.uya**: Файл, в который записывается результат преобразования.
- **README.md**: Документация проекта.

## Функциональность
Конвертер поддерживает следующие элементы YAML:

- **variable**: Определяет переменную, которая будет преобразована в строку формата `var NAME := VALUE;`.
- **constant**: Определяет константу, которая будет преобразована в строку формата `define NAME VALUE`.
- **array**: Определяет массив значений, который будет преобразован в строку формата `[ VALUE1, VALUE2, ... ]`.
- **len()**: Операция для вычисления длины массива.
- **pow()**: Операция для возведения числа в степень.

### Пример YAML
```yaml
library_name: "City Library"
books:
  - title: "The Great Gatsby"
    authors: ["F. Scott Fitzgerald"]
    pages: ".{ 10 20 + }."
  - title: "1984"
    authors: ["George Orwell"]
    pages: ".{ 50 50 - }."
categories: [ "Fiction", "Science", "Biography" ]
category_count: ".{ len([ 'Fiction', 'Science', 'Biography' ]) }."
average_pages: ".{ 2 3 pow() 2 / }."
```

Результаты 

```
var library_name 'City Library';
var books [ begin
 title := 'The Great Gatsby';
 authors := [ 'F. Scott Fitzgerald' ];
 pages := '.{ 10 20 + }.';
 end; begin
 title := '1984';
 authors := [ 'George Orwell' ];
 pages := '.{ 50 50 - }.';
 end ];
var categories [ 'Fiction'; 'Science'; 'Biography' ];
var category_count 3;
var average_pages 4.0;
```

Результат тестов