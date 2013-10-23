#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler

import logging
"""
create table Banner(
  title       varchar(255),
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Banner', (), size)
        self.results = self.sql.query_all('SELECT * FROM Banner ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        link = self.request.get('link') if self.request.get('link') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''
        self.sql.insert("Banner", {
            "title": title,
            "link": link,
            "content": content,
            "image": image,
            "is_enable": 1,
        })
        self.json({"info": u'輪撥圖已新增', "content": u"您已經成功的新增了一筆輪撥圖。"})


class Edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Banner where id = %s', id)

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        title = self.request.get('title') if self.request.get('title') is not None else u''
        link = self.request.get('link') if self.request.get('link') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''
        self.sql.update("Banner", {
            "title": title,
            "link": link,
            "content": content,
            "image": image,
        }, {
            "id": id
        })
        self.json({"info": u'輪撥圖已更新', "content": u"您已經成功的變更了此筆輪撥圖。"})
