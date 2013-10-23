#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Faq(
  title       varchar(500),
  content     mediumtext,
  create_date varchar(2000) NOT NULL,
  category    int not null,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;

create table FaqCategory(
  category_name    varchar(255),
  parent           int not null,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;
"""


class category_list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM FaqCategory', (), size)
        self.results = self.sql.query_all('SELECT * FROM FaqCategory ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)
        self.render("/admin/faq/category_list.html")


class category_create(AdministratorHandler):
    def get(self, *args):
        self.render("/admin/faq/category_create.html")

    def post(self, *args):
        self.sql.insert("FaqCategory", {
            "category_name": self.request.get('category_name') if self.request.get('category_name') is not None else u'',
            "parent": self.request.get('parent') if self.request.get('parent') is not None and self.request.get('parent') is not '' else 0,
            "is_enable": 1,
        })
        self.json({"info": u'問與答分類已新增', "content": u"您已經成功的新增了一筆問與答分類。"})


class category_edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM FaqCategory where id = %s', id)
        self.render("/admin/faq/category_edit.html")

    def post(self, *args):
        self.sql.update("FaqCategory", {
            "category_name": self.request.get('category_name') if self.request.get('category_name') is not None else u'',
            "parent": self.request.get('parent') if self.request.get('parent') is not None and self.request.get('parent') is not '' else 0,
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'問與答分類已更新', "content": u"您已經成功的變更了此筆問與答分類。"})


class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        str_category = self.request.get("category") if self.request.get("category") is not None and self.request.get("category") is not "" else u""
        if str_category is u"":
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq', (), size)
            self.results = self.sql.query_all('SELECT * FROM Faq ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)
        else:
            category = int(str_category)
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq Where category = %s', category, size)
            self.results = self.sql.query_all('SELECT * FROM Faq Where category = %s ORDER BY sort DESC LIMIT %s, %s', (category, (page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        self.results = self.sql.query_all('SELECT * FROM FaqCategory ORDER BY sort DESC')

    def post(self, *args):
        self.sql.insert("Faq", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "category": self.request.get('category') if self.request.get('category') is not None else u'',
            "content": self.request.get('content') if self.request.get('content') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'問與答已新增', "content": u"您已經成功的新增了一筆問與答。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Faq where id = %s', id)
        self.results = self.sql.query_all('SELECT * FROM FaqCategory ORDER BY sort DESC')
        for item in self.results:
            item["is_select"] = (self.record["category"] == item["id"])

    def post(self, *args):
        self.sql.update("Faq", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "content": self.request.get('content') if self.request.get('content') is not None else u'',
            "category": self.request.get('category') if self.request.get('category') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'問與答已更新', "content": u"您已經成功的變更了此筆問與答。"})