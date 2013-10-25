#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler


class Init(AdministratorHandler):
    def get(self, *args):
        self.sql.query_one("""
            create table Contact2(
                title       varchar(255),
                f1 text,
                f2_1_1  text,
                f2_1_2  text,
                f2_2_1  text,
                f2_2_2  text,
                f2_3_1  text,
                f2_3_2  text,
                f2_3_3  text,
                f2_3_4  text,
                f3  text,
                f4_1  text,
                f4_2  text,
                f4_3  text,
                f4_4  text,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Contact2', (), size)
        self.results = self.sql.query_all('SELECT * FROM Contact2 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class Edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Contact2 where id = %s', id)
