#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler


class Init(AdministratorHandler):
    def get(self):
        self.sql.query_one("""
            create table News(
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
        """)

        self.sql.query_one("""
            create table NewsCategory(
              category_name    varchar(255),
              parent           int not null,
              is_enable   tinyint(1),
              is_delete   tinyint(1) default 0,
              sort        timestamp default current_timestamp,
              id          int not null auto_increment,
              primary key (id)
            ) engine=myisam default charset=utf8;
            """)


class CategoryList(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM NewsCategory', (), size)
        self.results = self.sql.query_all('SELECT * FROM NewsCategory ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)
        self.render("/admin/news/category_list.html")


class CategoryCreate(AdministratorHandler):
    def get(self, *args):
        self.render("/admin/news/category_create.html")

    def post(self, *args):
        self.sql.insert("NewsCategory", {
            "category_name": self.params.get_string("category_name"),
            "parent": self.params.get_integer("parent"),
            "is_enable": 1,
        })
        self.json({"info": u'最新消息分類已新增', "content": u"您已經成功的新增了一筆最新消息分類。"})


class CategoryEdit(AdministratorHandler):
    def get(self, *args):
        id = self.params.get_string("id")
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM NewsCategory where id = %s', id)
        self.render("/admin/news/category_edit.html")

    def post(self, *args):
        self.sql.update("NewsCategory", {
            "category_name": self.params.get_string("category_name"),
            "parent": self.params.get_integer("parent"),
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'最新消息分類已更新', "content": u"您已經成功的變更了此筆最新消息分類。"})


class List(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        str_category = self.request.get("category") if self.request.get("category") is not None and self.request.get("category") is not "" else u""
        if str_category is u"":
            self.page_all = self.sql.pager('SELECT count(1) FROM News', (), size)
            self.results = self.sql.query_all('SELECT * FROM News ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)
        else:
            category = int(str_category)
            self.page_all = self.sql.pager('SELECT count(1) FROM News Where category = %s', category, size)
            self.results = self.sql.query_all('SELECT * FROM News Where category = %s ORDER BY sort DESC LIMIT %s, %s', (category, (page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
    def get(self, *args):
        from datetime import datetime
        self.today = datetime.today()
        self.results = self.sql.query_all('SELECT * FROM NewsCategory ORDER BY sort DESC')

    def post(self, *args):
        self.sql.insert("News", {
            "title": self.params.get_string("title"),
            "category": self.params.get_string("category"),
            "content": self.params.get_string("content"),
            "create_date": self.params.get_string("create_date"),
            "is_enable": '1',
        })
        self.json({"info": u'最新消息已新增', "content": u"您已經成功的新增了一筆最新消息。"})


class Edit(AdministratorHandler):
    def get(self, *args):
        id = self.params.get_string("id")
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM News where id = %s', id)
        self.results = self.sql.query_all('SELECT * FROM NewsCategory ORDER BY sort DESC')
        for item in self.results:
            item["is_select"] = (self.record["category"] == item["id"])

    def post(self, *args):
        self.sql.update("News", {
            "title": self.params.get_string("title"),
            "category": self.params.get_string("category"),
            "content": self.params.get_string("content"),
            "create_date": self.params.get_string("create_date")
        }, {
            "id": self.params.get_string("id")
        })
        self.json({"info": u'最新消息已更新', "content": u"您已經成功的變更了此筆最新消息。"})