#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=unused-import

"""context

Provides context to the backend modules
"""

from __future__ import absolute_import, print_function, unicode_literals
from os.path import abspath, dirname, join
import sys

MODULE_PATH = join(dirname(dirname(abspath(__file__))), "resquest", "src")
sys.path.append(MODULE_PATH)

import resquest
