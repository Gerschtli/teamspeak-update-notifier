#!/usr/bin/env bash
set -xe

pylama notifier tests
isort --check-only notifier/** tests/**
mypy notifier tests
