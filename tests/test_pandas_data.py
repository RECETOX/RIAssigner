import os
import pytest
from RIAssigner.data import PandasData


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def filename_csv():
    return os.path.join(here, "Alkanes_20210325.csv")


def test_none():
    pass


def test_has_filename(filename_csv):
    data = PandasData(filename_csv)
    assert data.filename == filename_csv
