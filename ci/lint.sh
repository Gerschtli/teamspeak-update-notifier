#!/usr/bin/env bash
set -xe

pylama notifier tests
mypy notifier tests
