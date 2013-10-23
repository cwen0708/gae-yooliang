#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26

import application
from application.backend.handler import AdministratorHandler
from google.appengine.api import users
from libs.yooframework.handler import BaseHandler
from libs.yooframework.environmentinfo import EnvironmentInfo
from libs.yooframework.database import *


class init(AdministratorHandler):
    def get(self):
        """ 後台"""
        user_agent_string = self.request.headers['user-agent']
        if user_agent_string.upper().find("MSIE") > 0:
            self.is_ie = True

        self.backend_path = u"/template/" + self.environ.theme_name + "/"
        self.backend_title = self.environ.customer_name
        self.backend_version = u"0.2.01"
        self.render("/v1/index.html", "backend")


class logout(AdministratorHandler):
    def get(self):
        self.session["administrator_email"] = ""
        url = users.create_logout_url("/admin")
        self.redirect(url)


class login_jump(BaseHandler):
    def get(self):
        self.render("/v1/login_jump.html", "backend")


class login(BaseHandler):
    def get(self):
        user = users.get_current_user()
        if users.is_current_user_admin() is True:
            self.session["administrator_account"] = user.email()
            self.session["administrator_email"] = user.email()
        else:
            self.login_text = u"登入"
            if user is not None:
                admin_user = self.sql.query_one('SELECT * FROM Administrator Where email = %s AND is_enable = 1', str(user.email()))
                if admin_user is not None:
                    self.session["administrator_account"] = admin_user["account"]
                    self.session["administrator_email"] = admin_user["email"]
                else:
                    self.login_message = u"" + str(user.email()) + u' <br />此帳號權限不足，請使用別的帳號重新登入'
                    self.administrator_login_url = users.create_logout_url("/admin")
                    self.login_text = u"登出"
                    self.render("/v1/login.html", "backend")
            else:
                self.session["administrator_account"] = u""
                self.session["administrator_email"] = u""


        if self.session["administrator_email"] is u"":
            self.login_message = u"請使用 Google 帳號登入"
            self.administrator_login_url = users.create_login_url("/admin")
            self.render("/v1//login.html", "backend")
        self.administrator_email = self.session["administrator_email"]

        if self.render("/v1/admin/index.html") is False:
            self.render('/v1/admin/index.html', "backend")
