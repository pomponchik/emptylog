# emptylog: some tools for logging

[![Downloads](https://static.pepy.tech/badge/emptylog/month)](https://pepy.tech/project/emptylog)
[![Downloads](https://static.pepy.tech/badge/emptylog)](https://pepy.tech/project/emptylog)
[![codecov](https://codecov.io/gh/pomponchik/emptylog/graph/badge.svg?token=I7Be1jVBeB)](https://codecov.io/gh/pomponchik/emptylog)
[![Lines of code](https://sloc.xyz/github/pomponchik/emptylog/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/emptylog?branch=main)](https://hitsofcode.com/github/pomponchik/emptylog/view?branch=main)
[![Test-Package](https://github.com/pomponchik/emptylog/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/emptylog/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/emptylog.svg)](https://pypi.python.org/pypi/emptylog)
[![PyPI version](https://badge.fury.io/py/emptylog.svg)](https://badge.fury.io/py/emptylog)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


This package ensures compatibility of any logger implementations with the built-in [`logging`](https://docs.python.org/3/library/logging.html) library.


## Table of contents

- [**Installing**](#installing)
- [**Universal Logger Protocol**](#universal-logger-protocol)
- [**Empty Logger**](#empty-logger)
- [**Memory Logger**](#memory-logger)
- [**Printing Logger**](#printing-logger)


## Installing

Install it from [Pypi](https://pypi.org/project/emptylog/):

```bash
pip install emptylog
```

You can also quickly try out this and other packages without having to install using [instld](https://github.com/pomponchik/instld).


## Universal Logger Protocol

Easily check whether an object is a logger using the protocol. The protocol contains 6 classic logger methods:

```python
def debug(message: str, *args: Any, **kwargs: Any) -> None: pass
def info(message: str, *args: Any, **kwargs: Any) -> None: pass
def warning(message: str, *args: Any, **kwargs: Any) -> None: pass
def error(message: str, *args: Any, **kwargs: Any) -> None: pass
def exception(message: str, *args: Any, **kwargs: Any) -> None: pass
def critical(message: str, *args: Any, **kwargs: Any) -> None: pass
```

The protocol is verifiable in runtime by the [`isinstance`](https://docs.python.org/3/library/functions.html#isinstance) function. Let's check this on a regular logger from `logging`:

```python
import logging
from emptylog import LoggerProtocol

print(isinstance(logging.getLogger('some_name'), LoggerProtocol))
#> True
```

This also works for third-party loggers with the same signature. Let's try it on [loguru](https://github.com/Delgan/loguru):

```python
from loguru import logger
from emptylog import LoggerProtocol

print(isinstance(logger, LoggerProtocol))
#> True
```

And of course, you can use the protocol for type hints:

```python
def function(logger: LoggerProtocol):
    logger.info('There was an earthquake in Japan, check the prices of hard drives!')
```

The protocol can be used for static checks by any tool you prefer, such as [`mypy`](https://github.com/python/mypy).


## Empty Logger

`EmptyLogger` is the simplest implementation of the [logger protocol](#universal-logger-protocol). When calling logging methods from an object of this class, nothing happens. You can use it as a stub, for example, when defining functions:

```python
from emptylog import EmptyLogger, LoggerProtocol

def function(logger: LoggerProtocol = EmptyLogger()):
    logger.error('Kittens have spilled milk, you need to pour more.')
```


## Memory Logger

`MemoryLogger` is a special class designed for tests. Its difference from [`EmptyLogger`](#empty-logger) is that it remembers all the times it was called.

The call history is stored in the `data` attribute and sorted by logger method names:

```python
from emptylog import MemoryLogger

logger = MemoryLogger()

logger.error('Joe Biden forgot his name again.')
logger.error('And again.')
logger.info("Joe, remember, you're Joe.")

print(logger.data)
#> LoggerAccumulatedData(debug=[], info=[LoggerCallData(message="Joe, remember, you're Joe.", args=(), kwargs={})], warning=[], error=[LoggerCallData(message='Joe Biden forgot his name again.', args=(), kwargs={}), LoggerCallData(message='And again.', args=(), kwargs={})], exception=[], critical=[])

print(logger.data.info[0].message)
#> Joe, remember, you're Joe.
print(logger.data.error[0].message)
#> Joe Biden forgot his name again.
print(logger.data.info[0].args)
#> ()
print(logger.data.info[0].kwargs)
#> {}
```

You can find out the total number of logs saved by `MemoryLogger` by applying the [`len()`](https://docs.python.org/3/library/functions.html#len) function to the `data` attribute:

```python
logger = MemoryLogger()

logger.warning("Are you ready, kids?")
logger.info("Aye, aye, Captain!")
logger.error("I can't hear you!")
logger.info("Aye, aye, Captain!")
logger.debug("Oh!")

print(len(logger.data))
#> 5
```


## Printing Logger

`PrintingLogger` is the simplest logger designed for printing to the console. You cannot control the format or direction of the output, or send logs to a special microservice that will forward them to a long-term storage with indexing support. No, here you can only get basic output to the console and nothing else. Here is an example:

```python
from emptylog import PrintingLogger

logger = PrintingLogger()

logger.debug("I ate a strange pill found under my grandfather's pillow.")
#> 2024-07-08 20:52:31.342048 | DEBUG     | I ate a strange pill found under my grandfather's pillow.
logger.info("Everything seems to be fine.")
#> 2024-07-08 20:52:31.342073 | INFO      | Everything seems to be fine.
logger.error("My grandfather beat me up. He seems to be breathing fire.")
#> 2024-07-08 20:52:31.342079 | ERROR     | My grandfather beat me up. He seems to be breathing fire.
```

As you can see, 3 things are output to the console: the exact time, the logging level, and the message. The message does not support extrapolation. Also, you won't see any additional arguments here that could have been passed to the method.

> ⚠️ Do not use this logger in production. It is intended solely for the purposes of debugging or testing of software.

If necessary, you can change the behavior of the logger by passing it a callback, which is called for the finished message to print it to the console. Instead of the original function (the usual [`print`](https://docs.python.org/3/library/functions.html#print) function is used under the hood), you can pass something more interesting (the code example uses the [`termcolor`](https://github.com/termcolor/termcolor) library):

```python
from termcolor import colored

def callback(string: str) -> None:
    print(colored(string, 'green'), end='')

logger = PrintingLogger(printing_callback=callback)

logger.info('Hello, the colored world!')
#> 2024-07-09 11:20:03.693837 | INFO      | Hello, the colored world!
# You can't see it here, but believe me, if you repeat the code at home, the output in the console will be green!
```
