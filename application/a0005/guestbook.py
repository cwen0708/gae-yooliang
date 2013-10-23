#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Guestbook(
  product_id         int not null,
  product_no         varchar(255),
  product_name       varchar(255),
  product_image      varchar(2000),
  member_id          int not null,
  member_name        varchar(255),
  contact_name       varchar(255),
  contact_telephone  varchar(255),
  contact_address    varchar(500),
  buy_date           varchar(255),
  create_date        varchar(255),
  content            text,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Guestbook', (), size)
        self.results = self.sql.query_all('SELECT * FROM Guestbook ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today() + datetime.timedelta(hours=+8)

    def post(self, *args):
        self.sql.insert("Guestbook", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "content": self.request.get('content') if self.request.get('content') is not None else u'',
            "create_date": self.request.get('create_date') if self.request.get('create_date') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'留言已新增', "content": u"您已經成功的新增了一筆留言。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        self.member = None
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Guestbook where id = %s', id)
            if self.record["member_id"] != '0':
                self.member = self.sql.query_one('SELECT * FROM Member where id = %s', self.record["member_id"])

    def post(self, *args):
        self.sql.update("Guestbook", {
            "reply": self.request.get('reply') if self.request.get('reply') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'留言已更新', "content": u"您已經成功的回覆了此筆留言。"})