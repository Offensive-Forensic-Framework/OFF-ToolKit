#!/usr/bin/env python

import os, sys, types

def color(string, status=True, warning=False, bold=True, blue=False):
    """
    Change text color for the linux terminal, defaults to green.
    Set "warning=True" for red.
    stolen from Veil :)
    """
    attr = []
    if status:
        # green
        attr.append('32')
    if warning:
        # red
        attr.append('31')
    if bold:
        attr.append('1')
    if blue:
        #blue
        attr.append('34')
    return '\x1b[%sm%s\x1b[0m' % (';'.join(attr), string)