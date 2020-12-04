#!/usr/bin/env python3

"""Main."""

import sys
from cpu import *
import os

cpu = CPU()

file_name = sys.argv[1]
FILEPATH = os.path.join(os.path.dirname(__file__), 'examples', file_name)
cpu.load(FILEPATH)
cpu.run()