from functools import wraps
from enum import Enum, unique
import sys
import datetime
import os
from typing import Any, Callable, Dict, Tuple, IO

assert IO


@unique
class PipeType(Enum):
    DEFAULT = 0

    BATCH_NUMBER = 10
    DATETIME = 20
    DATE_BATCH_NUMBER = 30
    DATE_HIERARCHY_BATCH_NUMBER = 40
    DATE_HIERARCHY_TIME = 50
    DATE_HIERARCHY_TIME_HIERARCHY_BATCH = 60
    FILENAME = 70


def pipe_to(
    *,
    base_path: str,
    pipe_type: PipeType = PipeType.DEFAULT,
    prefix: str = '',
    extension: str = 'txt',
    append: bool = False
) -> Callable:

    def get_next_batch_number(
        *,
        base_path: str
    ) -> int:
        # TODO JHILL: this is fugly but works, make it prettier
        file_numbers = []
        try:
            for f in os.listdir(base_path):
                filename = os.path.join(base_path, f)

                if not os.path.isfile(filename):
                    continue

                try:
                    filename = f.split(".")[0]
                    file_num = int(filename)
                    file_numbers.append(file_num)
                except ValueError as e:
                    pass
        except FileNotFoundError:
            pass
            
        next_batch_number = 1
        if len(file_numbers) != 0:
            next_batch_number = max(file_numbers) + 1
        return next_batch_number

    def get_pipe_destination(
        *,
        base_path: str,
        pipe_type: PipeType,
        prefix: str,
        extension: str
    ) -> str:
        base_path = os.path.expanduser(base_path)

        if pipe_type == PipeType.DEFAULT or pipe_type == PipeType.DATETIME:
            date, time = str(datetime.datetime.now()).split()
            base_path = os.path.join(base_path, date)

            if not os.path.exists(base_path):
                os.makedirs(base_path)
            return os.path.join(base_path, "{}{}.{}".format(prefix, time, extension))

        elif pipe_type == PipeType.BATCH_NUMBER:
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            next_batch_number = get_next_batch_number(base_path=base_path)

            return os.path.join(base_path, "{}{}.{}".format(prefix, str(next_batch_number), extension))

        elif pipe_type == PipeType.DATE_HIERARCHY_TIME:
            date, time = str(datetime.datetime.now()).split()
            date_components = date.split("-")

            base_path = os.path.join(base_path, date_components[0], date_components[1], date_components[2])
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            return os.path.join(base_path, "{}{}.{}".format(prefix, time, extension))

        elif pipe_type == PipeType.DATE_HIERARCHY_TIME_HIERARCHY_BATCH:
            date, time = str(datetime.datetime.now()).split()
            date_components = date.split("-")
            time_components = time.split(".")[0].split(":")

            base_path = os.path.join(
                base_path,
                date_components[0],
                date_components[1],
                date_components[2],
                time_components[0],
                time_components[1],
                time_components[2]
            )

            next_batch_number = get_next_batch_number(base_path=base_path)
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            return os.path.join(base_path, "{}{}.{}".format(prefix, next_batch_number, extension))

        elif pipe_type == PipeType.FILENAME:
            if os.path.isdir(base_path):
                raise ValueError("{} is a directory, this doesn't work".format(base_path))
            dirname = os.path.dirname(base_path)
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            return base_path

        elif pipe_type == PipeType.DATE_HIERARCHY_BATCH_NUMBER:
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            date, time = str(datetime.datetime.now()).split()
            date_components = date.split("-")

            base_path = os.path.join(base_path, date_components[0], date_components[1], date_components[2])
            if not os.path.exists(base_path):
                os.makedirs(base_path)

            next_batch_number = get_next_batch_number(base_path=base_path)

            return os.path.join(base_path, "{}{}.{}".format(prefix, str(next_batch_number), extension))

        elif pipe_type == PipeType.DATE_BATCH_NUMBER:
            date, time = str(datetime.datetime.now()).split()
            base_path = os.path.join(base_path, date)

            if not os.path.exists(base_path):
                os.makedirs(base_path)

            next_batch_number = get_next_batch_number(base_path=base_path)

            return os.path.join(base_path, "{}{}.{}".format(prefix, str(next_batch_number), extension))

        raise NotImplementedError

    def _impl(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Tuple, **kwargs: Dict) -> Any:
            current_stdout = sys.stdout
            

            if pipe_type == PipeType.FILENAME and prefix != '':
                raise ValueError("'prefix' not compatible with PipeType.FILENAME")
            elif pipe_type != PipeType.FILENAME and append is True:
                raise ValueError("'append' only compatible with PipeType.FILENAME")

            filename = get_pipe_destination(
                base_path=base_path,
                pipe_type=pipe_type,
                prefix=prefix,
                extension=extension
            )
            print('"pipe_to" is writing output of "{}" to {}'.format(func.__name__, filename))

            if append:
                sys.stdout = open(filename, 'a+')  # type: ignore
            else:
                sys.stdout = open(filename, 'w+')  # type: ignore
                
            return_value = func(*args, **kwargs)
            sys.stdout = current_stdout

            return return_value

        return wrapper
    return _impl
