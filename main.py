from pipe_to import pipe_to, PipeType


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.BATCH_NUMBER)
def batch_number() -> None:
    print("batch_number")


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.DATETIME)
def datetime() -> None:
    print("datetime")


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.DAY_HIERARCHY_TIME)
def day_hierarchy_time() -> None:
    print("day_hierarchy_time")


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.DAY_HIERARCHY_TIME_HIERARCHY)
def day_hierarchy_time_hierarchy() -> None:
    print("day_hierarchy_time_hieararchy")


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.FILENAME)
def filename_error_1() -> None:
    print("filename_error_1")


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.FILENAME, prefix="prefix")
def filename_error_2() -> None:
    print("filename_error_2")


@pipe_to(base_path='~/pipe_to_test/test.txt', pipe_type=PipeType.FILENAME)
def filename_success() -> None:
    print("filename_success")


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.DAY_HIERARCHY_TIME, append=True)
def append_error() -> None:
    print("append_error")


@pipe_to(base_path='~/pipe_to_test/', pipe_type=PipeType.DAY_HIERARCHY_BATCH_NUMBER)
def day_hierarchy_batch_number() -> None:
    print("day_hierarchy_batch_number")


if __name__ == '__main__':
    batch_number()
    datetime()
    day_hierarchy_time()
    day_hierarchy_time_hierarchy()
    try:
        filename_error_1()
    except ValueError as e:
        print(e)

    try:
        filename_error_2()
    except ValueError as e:
        print(e)

    filename_success()

    try:
        append_error()
    except ValueError as e:
        print(e)
        
    day_hierarchy_batch_number()