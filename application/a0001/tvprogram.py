#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table TVProgram(
  title       varchar(255),
  start_time  datetime,
  end_time    datetime,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM TVProgram', (), size)
        self.results = self.sql.query_all('SELECT * FROM TVProgram ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today()

    def post(self, *args):
        self.sql.insert("TVProgram", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'節目訊息已新增', "content": u"您已經成功的新增了一筆節目訊息。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM TVProgram where id = %s', id)

    def post(self, *args):
        self.sql.update("TVProgram", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'節目訊息已更新', "content": u"您已經成功的變更了此筆節目訊息。"})