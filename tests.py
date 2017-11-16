from freezegun import freeze_time
from main import (batch_number, datetime, date_hierarchy_batch_number, date_hierarchy_time,
                  date_hierarchy_time_hierarchy_batch, filename_error_1, filename_error_2, filename_success,
                  append_error, date_batch_number, append_success)

import os
import pytest


TEST_DIRECTORY = os.path.expanduser('~/pipe_to_test')


def test_batch_number() -> None:
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
def test_datetime() -> None:
    filename = os.path.join(TEST_DIRECTORY, '2015-01-01', '00:00:00.txt')
    if os.path.exists(filename):
        os.remove(filename)
    assert not os.path.exists(filename)

    datetime()
    assert os.path.exists(filename)

    with open(filename, "r") as f:
        assert f.read() == "datetime\n"


@freeze_time("2015-01-01")
def test_date_hierarchy_batch_number() -> None:
    for i in range(1, 100):
        filename = os.path.join(TEST_DIRECTORY, '2015', '01', '01', "{}.txt".format(i))
        if os.path.exists(filename):
            os.remove(filename)
        assert not os.path.exists(filename)

    for i in range(1, 100):
        date_hierarchy_batch_number()
        filename = os.path.join(TEST_DIRECTORY, '2015', '01', '01', "{}.txt".format(i))
        assert os.path.exists(filename)

        with open(filename, "r") as f:
            assert f.read() == "date_hierarchy_batch_number\n"


@freeze_time("2015-01-01")
def test_date_hierarchy_time() -> None:
    filename = os.path.join(TEST_DIRECTORY, '2015', '01', '01', "00:00:00.txt")
    if os.path.exists(filename):
        os.remove(filename)

    date_hierarchy_time()
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        assert f.read() == "date_hierarchy_time\n"


@freeze_time("2015-01-01")
def test_date_hierarchy_time_hierarchy_batch() -> None:
    for i in range(1, 100):
        filename = os.path.join(TEST_DIRECTORY, '2015', '01', '01', '00', '00', '00', "{}.txt".format(i))
        if os.path.exists(filename):
            os.remove(filename)

    for i in range(1, 100):
        date_hierarchy_time_hierarchy_batch()
        filename = os.path.join(TEST_DIRECTORY, '2015', '01', '01', '00', '00', '00', "{}.txt".format(i))

        assert os.path.exists(filename)
        with open(filename, "r") as f:
            assert f.read() == "date_hierarchy_time_hierarchy_batch\n"


def test_filename_error_1() -> None:
    with pytest.raises(ValueError):
        filename_error_1()


def test_filename_error_2() -> None:
    with pytest.raises(ValueError):
        filename_error_2()


def test_filename_success() -> None:
    filename = os.path.join(TEST_DIRECTORY, 'test.txt')
    if os.path.exists(filename):
        os.remove(filename)

    filename_success()
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        assert f.read() == "filename_success\n"


def test_append_error() -> None:
    with pytest.raises(ValueError):
        append_error()


def test_append_succes() -> None:
    filename = os.path.join(TEST_DIRECTORY, 'test.txt')
    if os.path.exists(filename):
        os.remove(filename)

    append_success()
    assert os.path.exists(filename)
    with open(filename, "r") as f:
        assert f.read() == "append_success\n"
    append_success()
    with open(filename, "r") as f:
        assert f.read() == "append_success\nappend_success\n"


@freeze_time("2015-01-01")
def test_date_batch_number() -> None:
    for i in range(1, 100):
        filename = os.path.join(TEST_DIRECTORY, '2015-01-01', "{}.txt".format(i))
        if os.path.exists(filename):
            os.remove(filename)

    for i in range(1, 100):
        filename = os.path.join(TEST_DIRECTORY, '2015-01-01', "{}.txt".format(i))
        date_batch_number()
        assert os.path.exists(filename)
        with open(filename, "r") as f:
            assert f.read() == "date_batch_number\n"
