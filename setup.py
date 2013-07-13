#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from cx_Freeze import setup, Executable


# GUI applications require a different base on Windows
#(the default is for a console application).
base = None
if sys.platform == "win32":
    base = "Win32GUI"

options = dict(
    compressed = True,
    includes = ["bipcomposer"],
    path = sys.path + ["modules"]
)

setup(name = "BipComposer",
      version = "2.0",
      description = "BipComposer",
      options = { "build_exe" : options },
      executables = [Executable("BipComposer.py", base=base)])
