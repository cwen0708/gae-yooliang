#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Solution(
  title       varchar(255),
  content     mediumtext,
  image       varchar(2000) NOT NULL,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;
"""


class List(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Solution', (), size)
        self.results = self.sql.query_all('SELECT * FROM Solution ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        self.sql.update("Solution", {
            "title": self.params.get_string("title"),
            "content": self.params.get_string("content"),
            "full_content": self.params.get_string("full_content"),
            "image": self.params.get_string("image"),
            "is_enable": 1,
        })
        self.json({"info": u'系統套案已新增', "content": u"您已經成功的新增了一筆系統套案。"})


class Edit(AdministratorHandler):
    def get(self, *args):
        self.record = self.sql.query_by_id("Solution", self.params.get_string("id"))

    def post(self, *args):
        self.sql.update("Solution", {
            "title": self.params.get_string("title"),
            "content": self.params.get_string("content"),
            "full_content": self.params.get_string("full_content"),
            "image": self.params.get_string("image"),
        }, {
            "id": self.params.get_string("id")
        })
        self.json({"info": u'系統套案已更新', "content": u"您已經成功的變更了此筆系統套案。"})
