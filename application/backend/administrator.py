#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26

from application.backend.handler import AdministratorHandler
from libs.yooframework.database import *
import logging
"""
create table Administrator(
  account     varchar(255),
  email       varchar(255) NOT NULL,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;
"""

class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Administrator', (), size)
        self.results = self.sql.query_all('SELECT * FROM Administrator ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)
        self.render("/v1/administrator/list.html", "backend")


class create(AdministratorHandler):
    def get(self, *args):
        self.render("/v1/administrator/create.html", "backend")

    def post(self, *args):
        account = self.request.get('account') if self.request.get('account') is not None else u''
        email = self.request.get('email') if self.request.get('email') is not None else u''

        if self.sql.query_one('SELECT * FROM Administrator where email = %s', email) is not None:
            self.json({"info": u'管理員帳號新增失敗', "content": u"此信箱已有人使用，請換一個。"})
            return

        self.sql.insert("Administrator", {
            "account": account,
            "email": email,
            "is_enable": '1',
        })
        self.json({"info": u'管理員帳號已新增', "content": u"您已經成功的新增了一筆管理員帳號。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Administrator where id = %s', id)
        self.render("/v1/administrator/edit.html", "backend")

    def post(self, *args):
        account = self.request.get('account') if self.request.get('account') is not None else u''
        email = self.request.get('email') if self.request.get('email') is not None else u''
        id = self.request.get('id') if self.request.get('id') is not None else ''

        if self.sql.query_one('SELECT * FROM Administrator where email = %s and id != %s', (email, id)) is not None:
            self.json({"info": u'管理員帳號新增失敗', "content": u"此信箱已有人使用，請換一個。"})
            return

        self.sql.update("Administrator", {
            "account": account,
            "email": email,
        }, {
            "id": id
        })
        self.json({"info": u'管理員帳號已更新', "content": u"您已經成功的變更了此筆管理員帳號。"})