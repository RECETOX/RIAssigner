from RIAssigner.data import MatchMSData


class MatchMSDataBuilder:

    def __init__(self):
        self.filename = None

    def with_filename(self, filename: str):
        self.filename = filename
        return self

    def build(self) -> MatchMSData:
        return MatchMSData(self.filename)
