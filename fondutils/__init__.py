#
# This file is part of fond-utils.
#
# Use of this source code is governed by an MIT-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/MIT.
#

"""Top-level package for fond-utils."""

# no need anymore, all automatic via setuptools-scm
# from .__version__ import (
#     version,
# )
from importlib.metadata import version
from .helpers.base import _get_current_path

_ROOT_PATH = _get_current_path()
VERSION = version("fond-utils")
