from pathlib import Path
import microbarometer as pm
from pytest import approx

R = Path(__file__).parent
ascfn = R / "sample.asc"


def test_load():
    dat = pm.load(ascfn)

    assert dat.iloc[123, 4] == approx(963895)
