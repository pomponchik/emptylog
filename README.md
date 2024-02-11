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

print(isinstance(logging.getLogger('some_name'), LoggerProtocol))  # True
```

This also works for third-party loggers with the same signature. Let's try it on [loguru](https://github.com/Delgan/loguru):

```python
from loguru import logger
from emptylog import LoggerProtocol

print(isinstance(logger, LoggerProtocol))  # True
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
