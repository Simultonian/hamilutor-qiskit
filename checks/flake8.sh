#!/usr/bin/env bash

folder=`dirname -- "$0"`
cd "$folder/.."
echo "Running pylint at $PWD"

# stop the build if there are Python syntax errors or undefined names
flake8 . --count --show-source --statistics
# exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
