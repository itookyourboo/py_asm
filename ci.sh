#!/bin/bash

echo '==[STATIC ANALYSIS]=='
echo '=====FLAKE8====='
flake8 .
echo '=====PYLINT====='
pylint ./main.py ./core/ ./test/
echo '======MYPY======'
mypy .

echo '==[TESTING]=='
echo '====UNIT-TESTS===='
pytest test/