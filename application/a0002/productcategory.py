#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table ProductCategory(
  category_name    varchar(255),
  parent           int not null,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;

"""


class list(AdministratorHandler):
    def get(self, *args):
        self.results = []
        pc = self.sql.query_all('SELECT * FROM ProductCategory Where parent = 0 ORDER BY sort DESC')
        for item in pc:
            item["is_not_root"] = False
            self.results.append(item)
            sc = self.sql.query_all('SELECT * FROM ProductCategory Where parent = %s ORDER BY sort DESC', item["id"])
            for item_sub in sc:
                item_sub["is_not_root"] = True
                self.results.append(item_sub)


class create(AdministratorHandler):
    def get(self, *args):
        self.results = self.sql.query_all('SELECT * FROM ProductCategory Where parent = 0 ORDER BY sort DESC')

    def post(self, *args):
        self.sql.insert('ProductCategory', {
            "category_name": self.request.get('title') if self.request.get('title') is not None else u'',
            "parent": self.request.get('parent') if self.request.get('parent') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'產品分類已新增', "content": u"您已經成功的新增了一筆產品分類。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM ProductCategory where id = %s', id)

        self.results = self.sql.query_all('SELECT * FROM ProductCategory Where parent = 0 ORDER BY sort DESC')
        for item in self.results:
            item["is_select"] = (self.record["parent"] == item["id"])

    def post(self, *args):
        self.sql.update('ProductCategory', {
            "category_name": self.request.get('title') if self.request.get('title') is not None else u'',
            "parent": self.request.get('parent') if self.request.get('parent') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'產品分類已更新', "content": u"您已經成功的變更了此筆產品分類。"})
