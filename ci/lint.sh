#!/usr/bin/env bash
set -xe

pycodestyle .
pyflakes .
find . -maxdepth 2 -type f -name "__init__.py" -exec dirname {} \; | \
  xargs -I % pylint --extension-pkg-whitelist=dependency_injector --disable=missing-docstring,too-few-public-methods %
