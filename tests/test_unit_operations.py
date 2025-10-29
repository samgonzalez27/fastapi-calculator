from app import operations


def test_add():
    assert operations.add(1, 2) == 3


def test_sub():
    assert operations.sub(5, 3) == 2


def test_mul():
    assert operations.mul(4, 2.5) == 10.0


def test_div():
    assert operations.div(10, 2) == 5


def test_div_by_zero_raises():
    try:
        operations.div(1, 0)
        assert False, "Expected ZeroDivisionError"
    except ZeroDivisionError:
        assert True
