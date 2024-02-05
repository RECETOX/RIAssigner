import os
import numpy
import pytest
from RIAssigner.compute import ComputationMethod, CubicSpline, Kovats
from RIAssigner.data import Data, SimpleData

from tests.fixtures import indexed_data, non_indexed_data, reference_alkanes
from tests.fixtures.data import load_test_file


here = os.path.abspath(os.path.dirname(__file__))
data_location = os.path.join(here, "data")

@pytest.mark.parametrize('this, other, expected', [
    [CubicSpline(), CubicSpline(), True],
    [Kovats(), Kovats(), True],
    [CubicSpline(), Kovats(), False],
    [Kovats(), object(), False],
    [CubicSpline(), object(), False],
])
def test_equal(this, other, expected):
    actual = (this == other)
    assert actual == expected


@pytest.mark.parametrize('method', [Kovats, CubicSpline])
def test_construct(method):
    compute = method()
    assert compute is not None


@pytest.mark.parametrize('method', [Kovats(), CubicSpline()])
@pytest.mark.parametrize("query, reference, message", [
    [SimpleData([10], "seconds", [100]), None, "Reference data is not defined."],
    [None, SimpleData([10], "seconds", [100]), "Query data is not defined."],
    [SimpleData([], "seconds", [100]), SimpleData([10], "seconds", [100]), "Query data has no retention times."],
    [SimpleData([10], "seconds", [100]), SimpleData([10], "seconds", []), "Reference data has no retention indices."],
    [SimpleData([10], "seconds", [100]), SimpleData([], "seconds", [10]), "Reference data has no retention times."],
])
def test_compute_exceptions(method: ComputationMethod, query: Data, reference: Data, message: str):
    with pytest.raises(ValueError) as exception:
        method.compute(query, reference)

    assert exception.typename == "ValueError"
    assert exception.value.args[0] == message


@pytest.mark.parametrize('method', [Kovats(), CubicSpline()])
@pytest.mark.parametrize('query_file, rt_unit', [
    ["aplcms_aligned_peaks.csv", "sec"],
    ["xcms_variable_metadata.csv", "sec"],
    ["PFAS_added_rt.msp", "sec"]
])
def test_computation(reference_alkanes, method, query_file, rt_unit):
    query = load_test_file(query_file, rt_unit)
    method_name = str(type(method).__name__).lower()
    results_path = os.path.join(data_location, method_name, os.path.splitext(query_file)[0] + ".npy")
    expected = numpy.load(results_path)

    actual = method.compute(query, reference_alkanes)
    numpy.testing.assert_array_almost_equal(actual, expected)
