#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler


class Init(AdministratorHandler):
    def get(self, *args):
        self.sql.query_one("""
            create table Aboutus(
              title       text,
              content     text,
              is_enable   tinyint(1),
              is_delete   tinyint(1) default 0,
              sort        timestamp default current_timestamp,
              id          int not null auto_increment,
              primary key (id)
            ) engine=myisam default charset=utf8;
            """)


class List(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Aboutus', (), size)
        self.results = self.sql.query_all('SELECT * FROM Aboutus ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        self.sql.insert("Aboutus", {
            "title": title,
            "content": content,
            "is_enable": 1,
        })
        self.json({"info": u'關於我們已新增', "content": u"您已經成功的新增了一筆關於我們。"})


class Edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Aboutus where id = %s', id)

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        self.sql.update("Aboutus", {
            "title": title,
            "content": content,
        }, {
            "id": id
        })
        self.json({"info": u'關於我們已更新', "content": u"您已經成功的變更了此筆關於我們。"})