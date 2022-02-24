import argparse

from RIAssigner.compute import CubicSpline, Kovats


class CreateMethodAction(argparse.Action):
    """Action to create 'ComputationMethod' instance."""
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        """ Interface has to be compatible with 'argparse.Action'. """
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Function to be called on action invocation

        Args:
            parser (argparse.ArgumentParser): Passed implicitly.
            namespace ([type]): Passed implicitly.
            values (str): Method name indicating which method to use.
            option_string (str, optional): Unused. Defaults to None.
        """
        if values not in ['kovats', 'cubicspline']:
            raise AssertionError("Method must be one of ['cubicspline', 'kovats'].")

        if values == "kovats":
            method = Kovats()
        elif values == "cubicspline":
            method = CubicSpline()

        setattr(namespace, self.dest, method)
