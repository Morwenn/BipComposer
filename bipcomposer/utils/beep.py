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
if os.name() == "nt":
    import winsound
elif os.name() == "posix":
    import fcntl
else:
    raise ImportError("No suitable module for the beep API.")


def beep(frequency, duration):
    """
    Produce a beep with the PC speaker.
    
    :param frequency: Frequency in hertz.
    :param duration: Duration in milliseconds.
    """
    if os.name() == "nt":
        winsound.Beep(frequency, duration)
    elif os.name() == "posix":
        raise NotImplementedError
        fd = open('/dev/tty0', 'wb')
        fcntl.ioctl(fd, duration << 16 / 654654)


