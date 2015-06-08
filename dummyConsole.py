#!/usr/bin/env python
# coding: utf-8

# a partial replacement for the Pythonista
# console module on non-Pythonista platforms

# necessary functions for this to work on the desktop independant of platform.

from __future__ import (absolute_import, division, print_function)

fmt = 'dummyConsole.{}():\n    Args: {!r}\n     {}'
kw_fmt = 'Key: {}\t\tValue: {!r}'

def hide_activity():
    pass

def show_activity():
    pass

def alert(*args, **kwargs):
    kw = (kw_fmt.format(k, v) for k, v in sorted(kwargs.iteritems()))
    print(fmt.format('alert', args, '\n     '.join(kw)))
    return 1  # it is always the first button!!

def hud_alert(*args, **kwargs):
    kw = (kw_fmt.format(k, v) for k, v in sorted(kwargs.iteritems()))
    print(fmt.format('hud_alert', args, '\n     '.join(kw)))
    
if __name__ == '__main__':
    print('=' * 20)
    hide_activity()
    show_activity()
    result = alert("Close", "Close File or Quit", "Close File", "Quit")
    print('Alert returned:', result)
    alert('With keywords', a = 0, b = 'b', c = ['c'])
    hud_alert('This is a hud_alert!')
    hud_alert('With keywords', a = 0, b = 'b', c = ['c'])

