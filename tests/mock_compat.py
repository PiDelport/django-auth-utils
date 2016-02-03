"""
unittest.mock backward compatibility.
"""
import sys

if sys.version_info < (3, 3):
    from mock import *  # noqa
else:
    from unittest.mock import *  # noqa
