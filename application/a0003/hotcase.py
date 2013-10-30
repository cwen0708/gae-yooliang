#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler


class Init(AdministratorHandler):
    def get(self, *args):
        self.sql.query_one("""
            create table HotCase(
              case_name   varchar(255),
              content     text,
              content_small text,
              images      text,
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
        self.page_all = self.sql.pager("SELECT count(1) FROM HotCase", (), size)
        self.results = self.sql.query_all("SELECT * FROM HotCase ORDER BY sort DESC LIMIT %s, %s", ((page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        self.sql.insert("HotCase", {
            "case_name": self.params.get_string("case_name"),
            "content": self.params.get_string("content"),
            "content_small": self.params.get_string("content_small"),
            "image": self.params.get_string("image"),
            "images": ",".join(self.params.get_list("images")),
            "is_enable": '1',
        })
        self.json({"info": u'熱銷專案已新增', "content": u"您已經成功的新增了一筆熱銷專案。"})


class Edit(AdministratorHandler):
    def get(self, *args):
        id = self.params.get_string("id")
        if id != u"":
            self.record = self.sql.query_one("SELECT * FROM HotCase where id = %s", id)
            if self.record["images"] is not None and self.record["images"] is not u"" and self.record["images"] is not "":
                self.images = self.record["images"].split(",")

    def post(self, *args):
        self.sql.update("HotCase", {
            "case_name": self.params.get_string("case_name"),
            "content": self.params.get_string("content"),
            "content_small": self.params.get_string("content_small"),
            "image": self.params.get_string("image"),
            "images": ",".join(self.params.get_list("images")),
        }, {
            "id": self.params.get_string("id")
        })
        self.json({"info": u'熱銷專案已更新', "content": u"您已經成功的變更了此筆熱銷專案。"})

