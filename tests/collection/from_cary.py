#! /usr/bin/env python3

import WrightTools as wt
from WrightTools import datasets

import pathlib

here = pathlib.Path(__file__).parent.resolve()


def test_CuPCtS_H2O_vis():
    p = datasets.Cary.CuPCtS_H2O_vis
    col = wt.collection.from_Cary(p)
    data = col.sample1
    assert col.natural_name == "cary"
    assert data.axis_names == ("wavelength",)
    assert data.units == ("nm",)
    assert data.shape == (141,)
    col.close()


def test_filters():
    p = datasets.Cary.filters
    col = wt.collection.from_Cary(p)
    assert len(col) == 11
    for d, sh in zip(col.values(), (121, 196, 301, 301, 301, 301, 301, 301, 301, 401, 101)):
        assert d.axis_names == ("wavelength",)
        assert d.channels[0].natural_name in ("abs", "%t")
        assert d.shape == (sh,)


def test_duplicate_name():
    p = here.parent / "data" / "test_data" / "duplicate_name.csv"
    col = wt.collection.from_Cary(p)
    assert len(col) == 2
    assert col.item_names == ("sample1_000", "sample1_001")
    col.close()


if __name__ == "__main__":
    test_CuPCtS_H2O_vis()
    test_filters()
    test_duplicate_name()
