#!/bin/sh
set -e -u

docker build --tag aoc-java .
docker run -v $PWD:/src/ aoc-java

