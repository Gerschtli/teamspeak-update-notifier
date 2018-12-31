#!/usr/bin/env bash
set -xe

pycodestyle                                                notifier tests
isort --check-only --recursive                             notifier tests
pyflakes                                                   notifier tests
pylint                                                     notifier
pylint -d broad-except,protected-access,too-many-arguments          tests
mypy                                                       notifier tests
