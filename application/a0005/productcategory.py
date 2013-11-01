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
        pc = self.sql.query_all('SELECT * FROM ProductCategory ORDER BY sort DESC')
        for item in pc:
            if item["parent"] == 0:
                item["level"] = 0
                item["in_list"] = True
                self.results.append(item)
            else:
                item["in_list"] = False
        # 最大３層
        pc_list = sorted(pc, reverse=True)
        for i in xrange(0, 3):
            for item in pc_list:
                if item["in_list"] is not True:
                    for parent_item in self.results:
                        if item["parent"] == parent_item["id"] and parent_item["level"] == i:
                            item["level"] = (i + 1)
                            item["in_list"] = True
                            index = self.results.index(parent_item) + 1
                            self.results.insert(index, item)



class create(AdministratorHandler):
    def get(self, *args):
        self.results = []
        pc = self.sql.query_all('SELECT * FROM ProductCategory ORDER BY sort DESC')
        for item in pc:
            if item["parent"] == 0:
                item["level"] = 0
                item["in_list"] = True
                self.results.append(item)
            else:
                item["in_list"] = False
        # 最大３層 下面略過
        for i in xrange(0, 2):
            for item in pc:
                if item["in_list"] is not True:
                    for parent_item in self.results:
                        if item["parent"] == parent_item["id"] and parent_item["level"] == i:
                            item["level"] = (i + 1)
                            item["in_list"] = True
                            index = self.results.index(parent_item) + 1
                            self.results.insert(index, item)


    def post(self, *args):
        member_discount_rate = self.params.get_float("member_discount_rate")
        if member_discount_rate < 0 or member_discount_rate > 100:
            self.json({"info": u'新增失敗', "content": u"會員折扣率必須介於 1~100 之間"})
            return
        seller_discount_rate = self.params.get_float("seller_discount_rate")
        if seller_discount_rate < 0 or seller_discount_rate > 100:
            self.json({"info": u'新增失敗', "content": u"經銷折扣率必須介於 1~100 之間"})
            return
        self.sql.insert('ProductCategory', {
            "category_name": self.request.get('title') if self.request.get('title') is not None else u'',
            "parent": self.params.get_string("parent"),
            "member_discount_rate": member_discount_rate,
            "seller_discount_rate": seller_discount_rate,
            "is_enable": '1',
        })
        self.json({"info": u'產品分類已新增', "content": u"您已經成功的新增了一筆產品分類。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM ProductCategory where id = %s', id)

        self.results = []
        pc = self.sql.query_all('SELECT * FROM ProductCategory ORDER BY sort DESC')
        for item in pc:
            if item["parent"] == 0:
                item["level"] = 0
                item["in_list"] = True
                self.results.append(item)
            else:
                item["in_list"] = False
        # 最大３層 下面略過
        for i in xrange(0, 2):
            for item in pc:
                if item["in_list"] is not True:
                    for parent_item in self.results:
                        if item["parent"] == parent_item["id"] and parent_item["level"] == i:
                            item["level"] = (i + 1)
                            item["in_list"] = True
                            index = self.results.index(parent_item) + 1
                            self.results.insert(index, item)

    def post(self, *args):
        member_discount_rate = self.params.get_float("member_discount_rate")
        if member_discount_rate < 0 or member_discount_rate > 100:
            self.json({"info": u'新增失敗', "content": u"會員折扣率必須介於 1~100 之間"})
            return
        seller_discount_rate = self.params.get_float("seller_discount_rate")
        if seller_discount_rate < 0 or seller_discount_rate > 100:
            self.json({"info": u'新增失敗', "content": u"經銷折扣率必須介於 1~100 之間"})
            return
        self.sql.update('ProductCategory', {
            "category_name": self.request.get('title') if self.request.get('title') is not None else u'',
            "parent": self.request.get('parent') if self.request.get('parent') is not None else u'',
            "member_discount_rate": member_discount_rate,
            "seller_discount_rate": seller_discount_rate,
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'產品分類已更新', "content": u"您已經成功的變更了此筆產品分類。"})
