from RIAssigner.data import MatchMSData


class MatchMSDataBuilder:

    def __init__(self):
        self.filename = None
        self._rt_unit = 'seconds'
        self._filetype = "msp"

    def with_filename(self, filename: str):
        self.filename = filename
        return self

    def with_rt_unit(self, rt_unit: str):
        self._rt_unit = rt_unit
        return self

    def with_filetype(self, filetype: str):
        self._filetype = filetype
        return self

    def build(self) -> MatchMSData:
        return MatchMSData(self.filename, self._filetype, self._rt_unit)
