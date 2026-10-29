# Seckill API Test

Interface automation test suite for the seckill system (pytest + requests + YAML).

## Setup

    pip install -r requirements.txt

## Run

    pytest
    pytest -m smoke
    pytest -m "not bug"

## Structure

    api/       HTTP client wrapper
    data/      YAML test data
    tests/     test cases
    conftest.py  fixtures