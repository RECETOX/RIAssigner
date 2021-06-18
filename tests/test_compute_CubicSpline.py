from RIAssigner.compute import CubicSpline


def test_construct():
    method = CubicSpline()
    assert method is not None