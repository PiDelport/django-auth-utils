#!/bin/sh -ex
# Run the tests with coverage reporting.

py.test --cov src --cov-report=html
