from io import StringIO
import pytest
from lab.main import main


def test_cli_add_student_flow(monkeypatch, capsys):
    """
    Эмулируем сценарий:
    1. Пользователь выбирает '4' (Добавить)
    2. Вводит ID '100'
    3. Вводит Имя 'New Student'
    4. Вводит Оценки '50 50'
    5. Выбирает '0' (Выход)
    """
    # Имитация ввода построчно
    inputs = iter([
        "4",  # Пункт меню
        "100",  # ID
        "New Student",  # Name
        "50 50",  # Grades
        "0"  # Exit
    ])

    # Подменяем функцию input() во всей программе на нашу заглушку
    monkeypatch.setattr('builtins.input', lambda msg="": next(inputs))

    # Запускаем main
    main()

    # Перехватываем всё, что программа вывела в консоль (print)
    captured = capsys.readouterr()

    assert "Студент успешно добавлен" in captured.out
    assert "Выход из программы" in captured.out