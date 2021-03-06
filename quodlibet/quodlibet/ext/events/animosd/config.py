# -*- coding: utf-8 -*-
# Copyright (C) 2012-13 Nick Boultbee, Thomas Vogt
# Copyright (C) 2008 Andreas Bombe
# Copyright (C) 2005  Michael Urman
# Based on osd.py (C) 2005 Ton van den Heuvel, Joe Wreshnig
#                 (C) 2004 Gustavo J. A. M. Carneiro
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of version 2 of the GNU General Public License as
# published by the Free Software Foundation.

from quodlibet.plugins import PluginConfig


def str_to_tuple(s):
    """Raises ValueError"""

    lst = map(float, s.split())
    while len(lst) < 4:
        lst.append(0.0)
    return tuple(lst)


def tuple_to_str(t):
    return " ".join(map(str, t))


DEFAULT_PATTERN = (r"<album|[b]<album>[/b]<discnumber| - Disc "
    """<discnumber>><part| - [b]<part>[/b]><tracknumber| - <tracknumber>>
    >[span weight='bold' size='large']<title>[/span] - <~length><version|
    [small][i]<version>[/i][/small]><~people|
    by <~people>>""")


class ConfProp(object):

    def __init__(self, conf, name, default):
        self._conf = conf
        self._name = name

        self._conf.defaults.set(name, default)

    def __get__(self, *args, **kwargs):
        return self._conf.get(self._name)

    def __set__(self, obj, value):
        self._conf.set(self._name, value)


class IntConfProp(ConfProp):

    def __get__(self, *args, **kwargs):
        return self._conf.getint(self._name)


class FloatConfProp(ConfProp):

    def __get__(self, *args, **kwargs):
        return self._conf.getfloat(self._name)


class ColorConfProp(object):

    def __init__(self, conf, name, default):
        self._conf = conf
        self._name = name

        self._conf.defaults.set(name, tuple_to_str(default))

    def __get__(self, *args, **kwargs):
        s = self._conf.get(self._name)

        try:
            return str_to_tuple(s)
        except ValueError:
            return str_to_tuple(self._conf.defaults.get(self._name))

    def __set__(self, obj, value):
        self._conf.set(self._name, tuple_to_str(value))


def get_config(prefix):
    class AnimOsdConfig(object):

        plugin_conf = PluginConfig(prefix)

        font = ConfProp(plugin_conf, "font", "Sans 22")
        string = ConfProp(plugin_conf, "string", DEFAULT_PATTERN)
        pos_y = FloatConfProp(plugin_conf, "pos_y", 0.0)
        corners = IntConfProp(plugin_conf, "corners", 1)
        delay = IntConfProp(plugin_conf, "delay", 2500)
        monitor = IntConfProp(plugin_conf, "monitor", 0)
        align = IntConfProp(plugin_conf, "align", 1)
        coversize = IntConfProp(plugin_conf, "coversize", 120)
        text = ColorConfProp(plugin_conf, "text", (0.9, 0.9, 0.9, 0.0))
        outline = ColorConfProp(plugin_conf, "outline", (-1.0, 0.0, 0.0, 0.2))
        shadow = ColorConfProp(plugin_conf, "shadow", (-1.0, 0.0, 0.0, 0.1))
        fill = ColorConfProp(plugin_conf, "fill", (0.25, 0.25, 0.25, 0.5))

    return AnimOsdConfig()
