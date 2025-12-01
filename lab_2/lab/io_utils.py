"""
Модуль ввода-вывода.
Отвечает за чтение и запись данных в формате CSV.
"""
import csv
import os
from typing import List
from lab.models import Student
from lab.errors import DataSourceError, ValidationError

def load_students_from_csv(filepath: str) -> List[Student]:
    """
    Загружает список студентов из CSV файла.
    Поддерживает файлы с заголовком и без.
    Формат: id, name, grade1, grade2, ...
    """
    if not os.path.exists(filepath):
        raise DataSourceError(f"Файл не найден: {filepath}")

    students = []

    try:
        with open(filepath, mode='r', encoding='utf-8', newline='') as f:
            reader = csv.reader(f)

            for row_idx, row in enumerate(reader, start=1):
                if not row:
                    continue  # Пропуск пустых строк

                # Очистка пробелов по краям ячеек
                row = [cell.strip() for cell in row]

                # Если первая колонка не число, считаем это заголовком и пропускаем
                if not row[0].isdigit():
                    print(f"Skipping header at line {row_idx}")
                    continue

                # Парсинг строки
                try:
                    # Минимум 2 колонки: id и name
                    if len(row) < 2:
                        raise ValueError("Недостаточно колонок (минимум ID и Имя).")

                    student_id = int(row[0])
                    name = row[1]

                    # Все остальные колонки — оценки. Пропускаем пустые.
                    grades = []
                    for val in row[2:]:
                        if val:
                            grades.append(int(val))

                    # Создаем объект
                    student = Student(student_id, name, grades)
                    students.append(student)

                except (ValueError, ValidationError) as e:
                    raise DataSourceError(f"Ошибка в строке {row_idx}: {e}")

    except OSError as e:
        raise DataSourceError(f"Ошибка доступа к файлу: {e}")

    return students

def save_students_to_csv(filepath: str, students: List[Student]):
    """
    Сохраняет список студентов в CSV.
    Выравнивает количество колонок оценок по максимуму в группе.
    """
    if not students:
        # Если список пуст, создаем пустой файл или файл только с заголовком
        try:
            with open(filepath, mode='w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["id", "name"])
            return
        except OSError as e:
            raise DataSourceError(f"Не удалось записать файл: {e}")

    # Определяем максимальное количество оценок для заголовка
    max_grades_count = max(len(s.grades) for s in students)

    # Формируем заголовок
    header = ["id", "name"] + [f"grade{i+1}" for i in range(max_grades_count)]

    try:
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for s in students:
                row = [s.id, s.name] + s.grades

                # Добиваем пустыми значениями, если оценок меньше максимума
                padding = [""] * (max_grades_count - len(s.grades))
                row.extend(padding)

                writer.writerow(row)

    except OSError as e:
        raise DataSourceError(f"Не удалось записать файл: {e}")

def export_top_students_to_csv(filepath: str, students: List[Student]):
    """
    Экспорт ТОП студентов в специальном формате.
    """
    header = ["id", "name", "average", "grades_str"]

    try:
        with open(filepath, mode='w', encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(header)

            for s in students:
                grades_str = " ".join(map(str, s.grades))

                row = [
                    s.id,
                    s.name,
                    f"{s.average_grade:.2f}",
                    grades_str
                ]
                writer.writerow(row)

    except OSError as e:
        raise DataSourceError(f"Не удалось экспортировать файл: {e}")