#!/usr/bin/env bash
set -xe

pycodestyle .
python -m pyflakes .
find . -maxdepth 2 -type f -name "__init__.py" -exec dirname {} \; | xargs -I % pylint %
