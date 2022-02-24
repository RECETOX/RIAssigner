import argparse

from RIAssigner.data import MatchMSData, PandasData


class LoadDataAction(argparse.Action):
    """Method to create a `Data` instance.
    Inherits from `argparse.Action`.
    """
    def __init__(self, option_strings, dest, **kwargs):
        """Constructor

        Args:
            option_strings (List[str]): See argparse.Action.
            dest (str): See argparse.Action.
        """
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        """Overloaded function from `argparse.Action` which is called upon invocation.

        Args:
            parser (argparse.ArgumentParser): Argument parser with args.
            namespace: namespace object.
            values (List[object]): Values passed as parameters to the Action.
            option_strings (List[str]): See argparse.Action.
        """
        filename = values[0]
        filetype = values[1]
        rt_unit = values[2]
        if filetype == 'msp':
            data = MatchMSData(filename, filetype, rt_unit)
        elif filetype in ['csv', 'tsv']:
            data = PandasData(filename, filetype, rt_unit)

        setattr(namespace, self.dest, data)
