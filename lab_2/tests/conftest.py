import pytest
from lab.models import Student

@pytest.fixture
def sample_students():
    return [
        Student(1, "Alice", [80, 90]),    # Avg: 85.0
        Student(2, "Bob", [60, 60, 60]),  # Avg: 60.0
        Student(3, "Charlie", [100]),     # Avg: 100.0
        Student(4, "Dave", []),           # Avg: 0.0
    ]