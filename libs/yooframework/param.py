#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/8/21
import os


class ParamInfo():
    def __init__(self, request):
        self.request = request

    def get_integer(self, key="", default_value=0):
        if key is "":
            return default_value
        try:
            if self.request.get(key) is None:
                return default_value
            _a = self.request.get(key) if int(self.request.get(key)) is not None else u''
            return default_value if _a == '' else int(_a)
        except:
            return default_value

    def get_float(self, key="", default_value=0.0):
        if key is "":
            return default_value
        try:
            if self.request.get(key) is None:
                return default_value
            _a = self.request.get(key) if int(self.request.get(key)) is not None else u''
            return default_value if _a == '' else float(_a)
        except:
            return default_value

    def get_string(self, key="", default_value=u''):
        if key is "":
            return default_value
        try:
            if self.request.get(key) is None:
                return default_value
            else:
                return self.request.get(key)
        except:
            return default_value

    def get_boolean(self, key="", default_value=False):
        if key is "":
            return default_value
        try:
            if self.request.get(key) is None:
                return default_value
            else:
                return bool(self.request.get(key))
        except:
            return default_value

    def get_list(self, key=""):
        list = []
        if key is not "":
            for item in self.request.POST.multi._items:
                if item[0] == key:
                    list.append(item[1])
        return list