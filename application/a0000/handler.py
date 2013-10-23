#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.yooframework.handler import BaseHandler
from webapp2_extras import sessions

class HomeHandler(BaseHandler):
    def app_init(self):
        if not self.is_localhost:
            self.config.template_render_from_cloud_storage = False
