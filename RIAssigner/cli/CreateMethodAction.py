from RIAssigner.compute import CubicSpline, Kovats


def create_method(method_name):
    """Create a computation method instance.

    Parameters
    ----------
    method_name : str
        Name of the method. Supported methods are 'kovats' and 'cubicspline'.

    Returns
    -------
    ComputationMethod
        Computation method instance.
    """
    if method_name == "kovats":
        return Kovats()
    elif method_name == "cubicspline":
        return CubicSpline()
    else:
        raise ValueError(f"Unsupported method: {method_name}. Supported methods are 'kovats' and 'cubicspline'.")
