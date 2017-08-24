# Description

A Python decorator that will display a progress flipper while a function runs.

# Installation

`pip install git+https://github.com/jonhillmtl/thread-flipper`

# Usage

```
from time import sleep
from thread_flipper import thread_flipper

@thread_flipper()
def main():
    sleep(5)

if __name__ == '__main__':
    main()
```