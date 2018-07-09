#!/usr/bin/env python
import pymicrobarometer as pm
import pytest


def test_import():
    assert pm is not None


if __name__ == '__main__':
    pytest.main()
