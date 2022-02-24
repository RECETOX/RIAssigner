import logging
from .__version__ import __version__


logging.getLogger(__name__).addHandler(logging.NullHandler())

__all__ = [
    "__version__",
]
