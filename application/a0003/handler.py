#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.yooframework.handler import BaseHandler
from webapp2_extras import sessions


class HomeHandler(BaseHandler):
    def app_init(self):
        self.is_ajax = self.params.get_boolean("isAjax")