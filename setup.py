#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This file is part of the BipComposer project.
# Copyright (C) 2013 Morwenn
# Contact: Morwenn <morwenn29@hotmail.fr>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA

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
