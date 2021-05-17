import os
import pytest
from RIAssigner.data import PandasData


here = os.path.abspath(os.path.dirname(__file__))


@pytest.fixture
def reference_alkanes():
    filename = os.path.join(here, os.pardir, "data", "csv", "Alkanes_20210325.csv")
    return PandasData(filename)


@pytest.fixture(params=["aplcms_aligned_peaks.csv", "xcms_variable_metadata.csv"])
def queries(request):
    _, extension = os.path.splitext(request.param)
    filename = os.path.join(here, os.pardir, "data", extension[1:], request.param)
    return PandasData(filename)
