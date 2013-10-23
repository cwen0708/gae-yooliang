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
        id = self.request.get('id') if self.request.get('id') is not None else ''
        self.customer_list = self.sql.query_all('SELECT * FROM Customer ORDER BY sort DESC')
        for i in self.customer_list:
            if i["id"] == str(id):
                i["is_select"] = True

        self.results = []
        pc = self.sql.query_all('SELECT * FROM CaseInfo Where customer_id = %s ORDER BY sort DESC', id)
        for item in pc:
            item["title"] = item["case_name"]
            item["is_not_root"] = False
            item["last_update"] = u""
            self.results.append(item)
            sc = self.sql.query_all('SELECT * FROM Equipment Where case_id = %s ORDER BY sort DESC', item["id"])
            for item_sub in sc:
                item_sub["title"] = item_sub["equipment_name"]
                item_sub["is_not_root"] = True
                self.results.append(item_sub)

class Create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''
        self.sql.insert("Banner", {
            "title": title,
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
        content = self.request.get('content') if self.request.get('content') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''
        self.sql.update("Aboutus", {
            "title": title,
            "content": content,
            "image": image,
        }, {
            "id": id
        })
        self.json({"info": u'輪撥圖已更新', "content": u"您已經成功的變更了此筆輪撥圖。"})
