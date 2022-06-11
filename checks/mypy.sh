#!/usr/bin/env bash

folder=`dirname -- "$0"`
cd "$folder/.."
echo "Running mypy at $PWD"
mypy .
