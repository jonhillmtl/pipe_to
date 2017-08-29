from freezegun import freeze_time
from functools import wraps
from main import batch_number, datetime, day_hierarchy_batch_number
from pipe_to import pipe_to, PipeType
from typing import Any, Callable, Tuple, Dict

import os
import shutil


TEST_DIRECTORY = os.path.expanduser('~/pipe_to_test')


def test_batch_number():    
    for i in range(1, 100):
        filename = os.path.join(TEST_DIRECTORY, "{}.txt".format(i))
        if os.path.exists(filename):
            os.remove(filename)
        assert not os.path.exists(filename)

    for i in range(1, 100):
        batch_number()
        filename = os.path.join(TEST_DIRECTORY, "{}.txt".format(i))
        assert os.path.exists(filename)

        with open(filename, "r") as f:
            assert f.read() == "batch_number\n"


@freeze_time("2015-01-01")
def test_datetime():
    filename = os.path.join(TEST_DIRECTORY, '2015-01-01', '00:00:00.txt')
    if os.path.exists(filename):
        os.remove(filename)
    assert not os.path.exists(filename)

    datetime()
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        assert f.read() == "datetime\n"


@freeze_time("2015-01-01")
def test_day_hierarchy_batch_number():
    for i in range(1, 100):
        filename = os.path.join(TEST_DIRECTORY, '2015', '01', '01', "{}.txt".format(i))
        if os.path.exists(filename):
            os.remove(filename)
        assert not os.path.exists(filename)

    for i in range(1, 100):
        day_hierarchy_batch_number()
        filename = os.path.join(TEST_DIRECTORY, '2015', '01', '01', "{}.txt".format(i))
        assert os.path.exists(filename)

        with open(filename, "r") as f:
            assert f.read() == "day_hierarchy_batch_number\n"
