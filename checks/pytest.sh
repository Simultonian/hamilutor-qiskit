#!/usr/bin/env bash

folder=`dirname -- "$0"`
cd "$folder/.."
echo "Running pytest at $PWD"
export PYTHONPATH=.
py.test
