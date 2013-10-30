#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler


class Init(AdministratorHandler):
    def get(self):
        self.sql.query_one("""
            create table Banner2(
              title       varchar(255),
              image       varchar(2000) NOT NULL,
              is_enable   tinyint(1),
              is_delete   tinyint(1) default 0,
              sort        timestamp default current_timestamp,
              id          int not null auto_increment,
              primary key (id)
            ) engine=myisam default charset=utf8;
            """)


class List(AdministratorHandler):
    def get(self):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Banner2', (), size)
        self.results = self.sql.query_all('SELECT * FROM Banner2 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
    def get(self):
        pass

    def post(self):
        self.sql.insert("Banner2", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "image": self.request.get('image') if self.request.get('image') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'輪撥圖已新增', "content": u"您已經成功的新增了一筆輪撥圖。"})


class Edit(AdministratorHandler):
    def get(self):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Banner where id = %s', id)

    def post(self):
        self.sql.update("Banner2", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "image": self.request.get('image') if self.request.get('image') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'輪撥圖已更新', "content": u"您已經成功的變更了此筆輪撥圖。"})

