#!/usr/bin/env bash
set -xe

pycodestyle .
pyflakes .
pylint --extension-pkg-whitelist=dependency_injector --disable=missing-docstring,too-few-public-methods notifier
pylint --extension-pkg-whitelist=dependency_injector --disable=missing-docstring,too-few-public-methods,invalid-name tests
mypy notifier tests --ignore-missing-imports
