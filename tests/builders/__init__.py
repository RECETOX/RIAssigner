import logging
from typing import Optional, Union

from .MatchMSDataBuilder import MatchMSDataBuilder
from .PandasDataBuilder import PandasDataBuilder
from .SimpleDataBuilder import SimpleDataBuilder

logging.getLogger(__name__).addHandler(logging.NullHandler())


def get_builder(filetype) -> Optional[Union[PandasDataBuilder, MatchMSDataBuilder]]:
    if (filetype in ['csv', 'tsv']):
        return PandasDataBuilder().with_filetype(filetype)
    if (filetype in ['msp']):
        return MatchMSDataBuilder().with_filetype(filetype)
    return None


__all__ = [
    "MatchMSDataBuilder",
    "PandasDataBuilder",
    "SimpleDataBuilder"
]
