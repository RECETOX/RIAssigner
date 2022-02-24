from RIAssigner.data import SimpleData


class SimpleDataBuilder():
    def __init__(self):
        self._rt = []
        self._ri = None
        self._rt_unit = "sec"

    def with_rt(self, rt):
        self._rt = rt
        return self

    def with_ri(self, ri):
        self._ri = ri
        return self

    def with_rt_unit(self, unit: str):
        self._rt_unit = unit
        return self
    
    def build(self):
        return SimpleData(self._rt, self._rt_unit, self._ri)

    
    
