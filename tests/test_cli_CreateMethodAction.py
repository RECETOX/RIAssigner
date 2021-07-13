import argparse

import pytest
from RIAssigner.cli import CreateMethodAction
from RIAssigner.compute import CubicSpline, Kovats


def load_method(method):
    if method == 'kovats':
        return Kovats()
    if method == 'cubicspline':
        return CubicSpline()
    return None


@pytest.mark.parametrize("method", ['kovats', 'cubicspline'])
def test_create_method(method):
    # Arrange
    expected = load_method(method)
    namespace = argparse.Namespace()
    parser = argparse.ArgumentParser()
    sut = CreateMethodAction("", "method")

    # Act
    sut(parser, namespace, method)
    actual = namespace.method

    # Assert
    # TODO: Implement comparison operator for computation methods
    assert isinstance(actual, type(expected))
