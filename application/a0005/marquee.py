#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Marquee(
  title       varchar(255),
  content     mediumtext,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;
"""


class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Marquee', (), size)
        self.results = self.sql.query_all('SELECT * FROM Marquee ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today()

    def post(self, *args):
        self.sql.insert("Marquee", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "content": self.request.get('content') if self.request.get('content') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'跑馬燈已新增', "content": u"您已經成功的新增了一筆跑馬燈。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Marquee where id = %s', id)

    def post(self, *args):
        self.sql.update("Marquee", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "content": self.request.get('content') if self.request.get('content') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'跑馬燈已更新', "content": u"您已經成功的變更了此筆跑馬燈。"})