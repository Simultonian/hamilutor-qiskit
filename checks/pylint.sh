#!/usr/bin/env bash

folder=`dirname -- "$0"`
cd "$folder/.."
echo "Running pylint at $PWD"

pylint $(git ls-files '*.py')
