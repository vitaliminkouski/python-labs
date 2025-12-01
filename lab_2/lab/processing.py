"""
Модуль обработки данных.
Содержит функции для расчета статистики, сортировки и выборки данных.
Реализован в стиле чистых функций (без побочных эффектов).
"""
from dataclasses import dataclass
from typing import List, Optional, Literal
from lab.models import Student

# Используем Literal для жесткой типизации стратегий сортировки
SortStrategy = Literal['id', 'name', 'avg']

@dataclass(frozen=True)
class GroupStats:
    """
    DTO (Data Transfer Object) для передачи статистики.
    frozen=True делает объект неизменяемым.
    """
    count: int
    overall_average: float
    best_student: Optional[Student]
    worst_student: Optional[Student]

def calculate_group_stats(students: List[Student]) -> GroupStats:
    """
    Рассчитывает статистику по группе студентов.
    """
    if not students:
        return GroupStats(0, 0.0, None, None)

    count = len(students)

    # Сбор всех оценок всех студентов в один плоский список
    all_grades = [g for s in students for g in s.grades]

    # Общий средний балл (сумма всех оценок / количество всех оценок)
    if all_grades:
        overall_avg = sum(all_grades) / len(all_grades)
    else:
        overall_avg = 0.0

    # Поиск лучшего и худшего по их личному среднему баллу
    best_student = max(students, key=lambda s: s.average_grade)
    worst_student = min(students, key=lambda s: s.average_grade)

    return GroupStats(
        count=count,
        overall_average=overall_avg,
        best_student=best_student,
        worst_student=worst_student
    )

def sort_students(students: List[Student], strategy: SortStrategy) -> List[Student]:
    """
    Сортирует список студентов согласно выбранной стратегии.
    """
    if strategy == 'id':
        return sorted(students, key=lambda s: s.id)

    elif strategy == 'name':
        return sorted(students, key=lambda s: s.name)

    elif strategy == 'avg':
        return sorted(students, key=lambda s: (-s.average_grade, s.name))

    else:
        # Если передан неизвестный ключ, возвращаем копию без сортировки
        return list(students)

def get_top_n_students(students: List[Student], n: int) -> List[Student]:
    """
    Возвращает топ N студентов по среднему баллу
    """
    if n <= 0:
        return []

    sorted_list = sort_students(students, 'avg')
    return sorted_list[:n]