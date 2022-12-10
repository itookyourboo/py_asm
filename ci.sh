#!/bin/bash

echo '==[STATIC ANALYSIS]=='
echo '=====FLAKE8====='
flake8 .
echo '=====PYLINT====='
pylint main.py
echo '======MYPY======'
mypy . --check-untyped-defs

echo '==[TESTING]=='
echo '====UNIT-TESTS===='
pytest test/