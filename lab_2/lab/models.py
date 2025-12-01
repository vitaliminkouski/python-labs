"""
Модуль с описанием моделей данных.
"""
from typing import List
from lab.errors import ValidationError

class Student:
    """
    Класс, описывающий студента.
    """

    def __init__(self, student_id: int, name: str, grades: List[int] = None):
        """
        Инициализация студента с валидацией данных.
        """
        self._validate_id(student_id)
        self._validate_name(name)

        if grades is None:
            grades = []
        self._validate_grades(grades)

        self._id = student_id
        self._name = name
        self._grades = grades

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def grades(self) -> List[int]:
        return self._grades

    @grades.setter
    def grades(self, new_grades: List[int]):
        self._validate_grades(new_grades)
        self._grades = new_grades

    @property
    def average_grade(self) -> float:
        if not self._grades:
            return 0.0
        return sum(self._grades) / len(self._grades)

    # Методы валидации

    def _validate_id(self, value: int):
        if not isinstance(value, int) or value <= 0:
            raise ValidationError(f"ID должен быть положительным целым числом. Получено: {value}")

    def _validate_name(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValidationError("Имя студента не может быть пустым.")

    def _validate_grades(self, values: List[int]):
        if not isinstance(values, list):
            raise ValidationError("Оценки должны быть списком.")
        for grade in values:
            if not isinstance(grade, int):
                raise ValidationError(f"Оценка должна быть целым числом. Получено: {grade}")
            if grade < 0 or grade > 100:
                raise ValidationError(f"Оценка должна быть в диапазоне 0-100. Получено: {grade}")

    def __str__(self):
        return f"Student(id={self.id}, name='{self.name}', avg={self.average_grade:.2f})"

    def __repr__(self):
        return self.__str__()