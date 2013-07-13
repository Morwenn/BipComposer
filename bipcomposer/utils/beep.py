#!/usr/bin/env python
# -*- coding: utf-8 -*-

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


