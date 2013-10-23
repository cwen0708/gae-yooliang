#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Partners(
  title       varchar(255),
  link        varchar(2000),
  image       varchar(2000) NOT NULL,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Partners', (), size)
        self.results = self.sql.query_all('SELECT * FROM Partners ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        self.sql.insert("Partners", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "link": self.request.get('link') if self.request.get('link') is not None else u'',
            "image": self.request.get('image') if self.request.get('image') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'合作廠商已新增', "content": u"您已經成功的新增了一筆合作廠商。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Partners where id = %s', id)

    def post(self, *args):
        self.sql.update("Partners", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "link": self.request.get('link') if self.request.get('link') is not None else u'',
            "image": self.request.get('image') if self.request.get('image') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'合作廠商已更新', "content": u"您已經成功的變更了此筆合作廠商。"})

