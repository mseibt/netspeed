#!/usr/bin/env python3

"""
Prints current (download) transfer for the device specified in DEVICE.
Uses the ifconfig command to retrieve the total amounts
of bytes sent since startup.
"""

import re
from subprocess import run, PIPE
import time

DEVICE = 'wlp3s0'


def current_bytes():
    """ return the total number of bytes since last reboot """
    proc = run('ifconfig', stdout=PIPE, stderr=PIPE, universal_newlines=True)
    output = proc.stdout
    output = output[output.find(DEVICE):]
    total_bytes = re.findall('RX bytes:([0-9]+) ', output)[0]
    return int(total_bytes)


if __name__ == '__main__':
    delta_seconds = 2
    start = current_bytes()

    while True:
        time.sleep(delta_seconds)

        stop = current_bytes()
        bytes_per_second = (stop-start)/delta_seconds
        kb_per_second = round(bytes_per_second / 1024, 4)
        start = stop

        print('{kbs} kB/s\033[K'.format(kbs=kb_per_second), end='\r')
