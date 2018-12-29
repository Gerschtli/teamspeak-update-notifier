#!/usr/bin/env bash
set -xe

pycodestyle .
pyflakes .
pylint --disable=missing-docstring,too-few-public-methods notifier
pylint --disable=missing-docstring,too-few-public-methods,invalid-name tests
mypy notifier tests
