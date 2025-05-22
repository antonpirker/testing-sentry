import random
import time

import pytest


@pytest.fixture()
def my_fixture():
    time.sleep(random.random())


def test_always_succeeds(my_fixture):
    assert True


def test_flaky():
    if random.random() < 0.80:
        assert False, "This is a flaky test"

    assert True


def test_always_fails():
    assert False
