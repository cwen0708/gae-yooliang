#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26


import os

from webapp2_extras import sessions
from google.appengine.api import users
import jinja2

from libs.yooframework.database import *
from libs.yooframework.handler import BaseHandler


class AdministratorHandler(BaseHandler):
    def app_init(self):
        """ 需要管理員身份才可執行 """
        user = users.get_current_user()
        self.login_text = u"登入"
        if "administrator_email" not in self.session or self.session["administrator_email"] == u"":
            if user is not None:
                admin_user = self.sql.query_one('SELECT * FROM Administrator Where email = %s AND is_enable = 1', str(user.email()))
                if admin_user is not None:
                    self.session["administrator_account"] = admin_user["account"]
                    self.session["administrator_email"] = admin_user["email"]
                else:
                    if users.is_current_user_admin() is True:
                        self.session["administrator_email"] = user.email()
                        self.session["administrator_account"] = user.email()
                    else:
                        self.session["administrator_email"] = u""
                        self.session["administrator_account"] = u""
            else:
                self.session["administrator_email"] = u""
                self.session["administrator_account"] = u""

        if self.session["administrator_email"] is u"":
            self.redirect("/admin/login_jump.html")
            return
        try:
            self.administrator_account = self.session["administrator_account"]
            if self.administrator_account is u"":
                self.administrator_account = self.session["administrator_email"]
        except:
            self.administrator_account = self.session["administrator_email"]