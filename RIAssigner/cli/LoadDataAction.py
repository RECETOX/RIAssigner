import argparse

from RIAssigner.utils import get_extension
from RIAssigner.data import MatchMSData, PandasData


class LoadDataAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        filetype = get_extension(values)
        if filetype == '.msp':
            data = MatchMSData(values)
        elif filetype == '.csv':
            data = PandasData(values)

        setattr(namespace, self.dest, data)
