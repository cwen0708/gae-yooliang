#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
from datetime import datetime
import logging
import time
"""
create table Contact(
    title       varchar(255),
    contact_name  text,
    contact_tel  text,
    contact_address  text,
    contact_want_1  text,
    contact_want_2  text,
    contact_mail  text,
    roof_materials  text,
    power_number  text,
    roof_objects_1  text,
    roof_objects_2  text,
    floor_area_1  text,
    floor_area_2  text,
    floor_area_3  text,
    floor_area_4  text,
    floor_area_5  text,
    floor_area_outside  text,
    floor_area_other  text,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Contact', (), size)
        self.results = self.sql.query_all('SELECT * FROM Contact ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Contact where id = %s', id)
