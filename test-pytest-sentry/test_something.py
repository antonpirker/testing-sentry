import random


def test_flaky():
    if random.randint(0, 100) > 50:
        assert 4 == 0, "4This is a flaky test"

    assert 1 == 1
