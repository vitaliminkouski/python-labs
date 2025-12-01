"""
Точка входа в консольное приложение.
Управляет меню, вводом пользователя и связывает все модули.
"""
import sys
import os
from typing import List

# Импорты из наших модулей
from lab.models import Student
from lab.errors import AppError, StudentNotFoundError
import lab.io_utils as io
import lab.processing as proc


# Вспомогательные функции ввода

def get_input(prompt: str) -> str:
    """Обертка над input для упрощения моков в тестах."""
    return input(prompt).strip()


def get_int_input(prompt: str) -> int:
    """Запрашивает целое число, повторяет запрос при ошибке."""
    while True:
        value = get_input(prompt)
        try:
            return int(value)
        except ValueError:
            print("Ошибка: Введите целое число.")


def get_grades_input(prompt: str) -> List[int]:
    """
    Запрашивает строку оценок через пробел и преобразует в список.
    """
    while True:
        value = get_input(prompt)
        if not value:
            return []
        try:
            return [int(x) for x in value.split()]
        except ValueError:
            print("Ошибка: Оценки должны быть целыми числами, разделенными пробелом.")


# Обработчики команд меню

def print_table(students: List[Student]):
    """Выводит список студентов в виде простой таблицы."""
    if not students:
        print("Список студентов пуст.")
        return

    print(f"{'ID':<5} {'Имя':<25} {'Ср.балл':<10} {'Оценки'}")
    print("-" * 60)
    for s in students:
        grades_str = ", ".join(map(str, s.grades))
        print(f"{s.id:<5} {s.name:<25} {s.average_grade:<10.2f} [{grades_str}]")
    print("-" * 60)
    print(f"Всего: {len(students)}")


def handle_add(students: List[Student]):
    print("\n--- Добавление студента ---")
    try:
        new_id = get_int_input("Введите ID: ")

        # Проверка на дубликат ID
        if any(s.id == new_id for s in students):
            print(f"Ошибка: Студент с ID {new_id} уже существует.")
            return

        name = get_input("Введите ФИО: ")
        grades = get_grades_input("Введите оценки через пробел (Enter, если нет): ")

        # Создание объекта (тут сработает валидация из models.py)
        new_student = Student(new_id, name, grades)
        students.append(new_student)
        print("Студент успешно добавлен.")

    except AppError as e:
        print(f"Ошибка валидации: {e}")


def handle_remove(students: List[Student]):
    print("\n--- Удаление студента ---")
    target_id = get_int_input("Введите ID для удаления: ")

    # Ищем индекс студента
    found_idx = -1
    for i, s in enumerate(students):
        if s.id == target_id:
            found_idx = i
            break

    if found_idx != -1:
        removed = students.pop(found_idx)
        print(f"Студент {removed.name} (ID: {removed.id}) удален.")
    else:
        print(f"Ошибка: Студент с ID {target_id} не найден.")


def handle_update_grades(students: List[Student]):
    print("\n--- Обновление оценок ---")
    target_id = get_int_input("Введите ID студента: ")

    # Поиск студента
    student = next((s for s in students if s.id == target_id), None)

    if student:
        print(f"Текущие оценки для {student.name}: {student.grades}")
        try:
            new_grades = get_grades_input("Введите новые оценки (перезапишут старые): ")
            student.grades = new_grades  # Сеттер выполнит валидацию
            print("Оценки обновлены.")
        except AppError as e:
            print(f"Не удалось обновить: {e}")
    else:
        print(f"Ошибка: Студент с ID {target_id} не найден.")


def handle_stats(students: List[Student]):
    print("\n--- Статистика группы ---")
    stats = proc.calculate_group_stats(students)

    if stats.count == 0:
        print("Нет данных для статистики.")
    else:
        print(f"Количество студентов: {stats.count}")
        print(f"Общий средний балл:  {stats.overall_average:.2f}")
        print(f"Лучший студент:      {stats.best_student.name} ({stats.best_student.average_grade:.2f})")
        print(f"Худший студент:      {stats.worst_student.name} ({stats.worst_student.average_grade:.2f})")


def handle_top_export(students: List[Student]):
    print("\n--- Экспорт ТОП-N ---")
    n = get_int_input("Сколько лучших студентов сохранить? ")
    # Если пользователь просто нажал Enter, имя будет "top.csv"
    filename = get_input("Имя файла для экспорта (например, top.csv): ") or "top.csv"

    top_students = proc.get_top_n_students(students, n)

    try:
        io.export_top_students_to_csv(filename, top_students)
        print(f"Успешно сохранено {len(top_students)} записей в {filename}")
    except AppError as e:
        print(f"Ошибка экспорта: {e}")


# Основной цикл

def print_menu():
    print("\n=== МЕНЮ УПРАВЛЕНИЯ СТУДЕНТАМИ ===")
    print("1. Загрузить из CSV")
    print("2. Сохранить в CSV")
    print("3. Показать всех")
    print("4. Добавить студента")
    print("5. Удалить по ID")
    print("6. Обновить оценки по ID")
    print("7. Статистика группы")
    print("8. Сортировка списка")
    print("9. Экспорт ТОП-N")
    print("0. Выход")


def main():
    # Состояние приложения (список студентов)
    current_students: List[Student] = []

    while True:
        print_menu()
        choice = get_input("Ваш выбор: ")

        try:
            if choice == '1':
                path = get_input("Путь к файлу [data/students.csv]: ") or "data/students.csv"
                current_students = io.load_students_from_csv(path)
                print('-' * 60)
                print(f"Загружено {len(current_students)} студентов.")
                print('-' * 60)

            elif choice == '2':
                path = get_input("Путь для сохранения [data/output.csv]: ") or "data/output.csv"
                io.save_students_to_csv(path, current_students)
                print('-' * 60)
                print("Файл успешно сохранен.")
                print('-' * 60)

            elif choice == '3':
                print('-' * 60)
                print_table(current_students)
                print('-' * 60)

            elif choice == '4':
                handle_add(current_students)

            elif choice == '5':
                handle_remove(current_students)

            elif choice == '6':
                print('-' * 60)
                handle_update_grades(current_students)
                print('-' * 60)

            elif choice == '7':
                print('-' * 60)
                handle_stats(current_students)
                print('-' * 60)

            elif choice == '8':
                print('-' * 60)
                print("Критерии: id, name, avg")
                key = get_input("Введите критерий сортировки: ")

                current_students = proc.sort_students(current_students, key)
                print("Список отсортирован.")
                print_table(current_students)

            elif choice == '9':
                print('-' * 60)
                handle_top_export(current_students)
                print('-' * 60)

            elif choice == '0':
                print("Выход из программы.")
                break

            else:
                print("Неверный пункт меню, повторите ввод.")

        except AppError as e:
            print(f"!!! ОШИБКА ОПЕРАЦИИ: {e}")
        except Exception as e:
            # Перехват непредвиденных ошибок (чтобы программа не упала с traceback)
            print(f"!!! КРИТИЧЕСКАЯ ОШИБКА: {e}")
            # В реальном приложении тут был бы логгинг: logging.exception(e)


if __name__ == "__main__":

    try:
        main()
    except KeyboardInterrupt:
        print("\nПринудительное завершение работы.")
