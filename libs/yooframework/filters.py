#!/usr/bin/env python
# -*- coding: utf-8 -*-
import application


def datetime_timesp(value):
    from datetime import timedelta
    import time
    try:
        d = value + timedelta(hours=+8)
        return time.mktime(d.timetuple())
    except :
        return 0.0


def datetime_format(value, format ="%Y/%m/%d %H:%M"):
    from datetime import timedelta

    try:
        d = value + timedelta(hours=+8)
        return d.strftime(format)
    except :
        return "datetime error"


def static_path(value):
    return u"/static/" + application.get_theme() + u"/" + value


def absolute_path(value):
    return value


def __temp__001__():
    import datetime
    d = datetime.datetime.now()
    from libs.dateutil.relativedelta import relativedelta
    d = d + relativedelta(hour=8)