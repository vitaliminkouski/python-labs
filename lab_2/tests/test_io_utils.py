import pytest
from lab.io_utils import save_students_to_csv, load_students_from_csv
from lab.errors import DataSourceError


def test_roundtrip_csv(tmp_path, sample_students):
    """Проверка цикла: Сохранить -> Загрузить -> Сравнить"""
    file_path = tmp_path / "students.csv"

    # Сохраняем
    save_students_to_csv(str(file_path), sample_students)
    assert file_path.exists()

    # Загружаем обратно
    loaded = load_students_from_csv(str(file_path))

    assert len(loaded) == len(sample_students)
    assert loaded[0].name == sample_students[0].name
    # Проверка восстановления оценок
    assert loaded[0].grades == sample_students[0].grades


def test_load_not_found():
    with pytest.raises(DataSourceError, match="Файл не найден"):
        load_students_from_csv("non_existent_file.csv")


def test_load_bad_format(tmp_path):
    f = tmp_path / "bad.csv"
    # Изменяем данные теста:
    # ID = 1 (валидный, программа начнет читать строку)
    # Оценка = "abc" (невалидная, программа упадет при попытке int("abc"))
    f.write_text("id,name,grade1\n1,Ivan,abc")

    with pytest.raises(DataSourceError):
        load_students_from_csv(str(f))