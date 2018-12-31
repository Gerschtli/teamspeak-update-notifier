#!/usr/bin/env bash
set -xe

pycodestyle .
pyflakes .
pylint notifier tests
isort --check-only notifier/** tests/**
mypy notifier tests
