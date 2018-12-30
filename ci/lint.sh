#!/usr/bin/env bash
set -xe

pycodestyle .
pyflakes .
pylint notifier tests
mypy notifier tests
