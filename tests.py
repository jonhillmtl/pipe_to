from pipe_to import pipe_to, PipeType
from freezegun import freeze_time
from main import batch_number
from typing import Any, Callable, Tuple, Dict
from functools import wraps
import shutil
import os

def clear_directory(base_path: str = '~/pipe_to_test'):
    def _impl(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Tuple, **kwargs: Dict) -> Any:
            return func(*args, **kwargs)
        return wrapper
    return _impl
    
@clear_directory()
def test():
    batch_number()
    