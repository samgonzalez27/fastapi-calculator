from app import calculator


def test_add():
    assert calculator.add(1, 2) == 3


def test_sub():
    assert calculator.sub(5, 3) == 2


def test_mul():
    assert calculator.mul(4, 2.5) == 10.0


def test_div():
    assert calculator.div(10, 2) == 5


def test_div_by_zero_raises():
    try:
        calculator.div(1, 0)
        assert False, "Expected ZeroDivisionError"
    except ZeroDivisionError:
        assert True
