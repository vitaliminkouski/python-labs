from lab.processing import calculate_group_stats, sort_students, get_top_n_students


def test_calculate_stats(sample_students):
    stats = calculate_group_stats(sample_students)

    assert stats.count == 4
    # overall_average считается как сумма ВСЕХ оценок / кол-во ВСЕХ оценок
    # Оценки: 80, 90, 60, 60, 60, 100. Сумма: 450. Кол-во: 6.
    # 450 / 6 = 75.0
    assert stats.overall_average == 75.0
    assert stats.best_student.name == "Charlie"  # Avg 100
    assert stats.worst_student.name == "Dave"  # Avg 0


def test_sort_by_avg(sample_students):
    sorted_list = sort_students(sample_students, 'avg')
    # Ожидаемый порядок: Charlie (100), Alice (85), Bob (60), Dave (0)
    assert sorted_list[0].name == "Charlie"
    assert sorted_list[1].name == "Alice"
    assert sorted_list[-1].name == "Dave"


def test_sort_by_name(sample_students):
    sorted_list = sort_students(sample_students, 'name')
    assert sorted_list[0].name == "Alice"
    assert sorted_list[-1].name == "Dave"


def test_get_top_n(sample_students):
    top = get_top_n_students(sample_students, 2)
    assert len(top) == 2
    assert top[0].name == "Charlie"
    assert top[1].name == "Alice"