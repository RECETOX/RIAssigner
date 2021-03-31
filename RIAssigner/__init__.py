
import logging
from .__version__ import __version__


logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Helge Hecht"
__email__ = 'helge.hecht@recetox.muni.cz'
__all__ = [
    "__version__",
]