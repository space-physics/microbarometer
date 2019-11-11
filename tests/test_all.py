#!/usr/bin/env python
from pathlib import Path
import microbarometer as pm
import pytest
from pytest import approx

R = Path(__file__).parent
ascfn = R / 'sample.asc'


def test_load():
    dat = pm.load(ascfn)

    assert dat.iloc[123, 4] == approx(963895)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
