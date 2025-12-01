import pytest
from lab.models import Student
from lab.errors import ValidationError


def test_student_creation_valid():
    s = Student(1, "Ivan", [10, 20, 30])
    assert s.id == 1
    assert s.name == "Ivan"
    assert s.grades == [10, 20, 30]
    assert s.average_grade == 20.0


def test_student_average_empty():
    s = Student(2, "Petr")
    assert s.grades == []
    assert s.average_grade == 0.0


def test_validation_id():
    with pytest.raises(ValidationError):
        Student(-1, "Bad ID")


def test_validation_name():
    with pytest.raises(ValidationError):
        Student(1, "")  # Пустое имя


def test_validation_grades():
    with pytest.raises(ValidationError):
        Student(1, "Oleg", [105])  # Оценка > 100

    with pytest.raises(ValidationError):
        Student(1, "Oleg", [-5])  # Оценка < 0


def test_grades_setter_validation():
    s = Student(1, "Ok")
    with pytest.raises(ValidationError):
        s.grades = [200]  # Попытка присвоить плохие оценки