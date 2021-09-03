import argparse

from RIAssigner.data import MatchMSData, PandasData


class LoadDataAction(argparse.Action):
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        filename = values[0]
        filetype = values[1]
        rt_unit = values[2]
        if filetype == 'msp':
            data = MatchMSData(filename, filetype, rt_unit)
        elif filetype in ['csv', 'tsv']:
            data = PandasData(filename, filetype, rt_unit)

        setattr(namespace, self.dest, data)
