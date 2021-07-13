from RIAssigner.data.PandasData import PandasData
import argparse
import os.path
import pytest

from RIAssigner.cli import LoadDataAction
from RIAssigner.data import MatchMSData
from tests.fixtures.data import data_location


def test_create():
    sut = LoadDataAction("", "")
    assert sut is not None


def test_load_data_pandas():
    filename = os.path.join(data_location, "csv", "Alkanes_20210325.csv")
    expected = PandasData(filename)
    namespace = argparse.Namespace()
    parser = argparse.ArgumentParser()
    sut = LoadDataAction("", "data")

    sut(parser, namespace, filename)
    actual = namespace.data
    assert actual == expected
