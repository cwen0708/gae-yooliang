#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Product(
  product_name    varchar(500),
  parent_category int not null,
  category    int not null,
  product_no    varchar(500),
  original_price   float default 0,
  selling_price   float default 0,
  image    text,
  images    text,
  content text,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Product', (), size)
        self.results = self.sql.query_all('SELECT * FROM Product ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
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

    def post(self, *args):
        category = self.params.get_string("category")
        category_record = self.sql.query_one('SELECT * FROM ProductCategory where id = %s', category)

        self.sql.insert("Product", {
            "product_name": self.params.get_string("product_name"),
            "product_no": self.params.get_string("product_no"),
            "content": self.params.get_string("content"),
            "parent_category": category_record["parent"],
            "price": self.params.get_string("price"),
            "images": ",".join(self.params.get_list("images")),
            "image": self.params.get_string("image"),
            "category": category,
            "is_enable": '1',
        })
        self.json({"info": u'產品已新增', "content": u"您已經成功的新增了一筆產品。"})


class Edit(AdministratorHandler):
    def get(self, *args):
        record_id = self.params.get_string("id")
        if record_id != '':
            self.record = self.sql.query_one('SELECT * FROM Product where id = %s', record_id)

        self.results = []
        pc = self.sql.query_all('SELECT * FROM ProductCategory Where parent = 0 ORDER BY sort DESC')
        for item in pc:
            item["is_not_root"] = False
            self.results.append(item)
            sc = self.sql.query_all('SELECT * FROM ProductCategory Where parent = %s ORDER BY sort DESC', item["id"])
            for item_sub in sc:
                item_sub["is_not_root"] = True
                item_sub["is_select"] = (int(self.record["category"]) == int(item_sub["id"]))
                self.results.append(item_sub)

        if self.record["images"] is not None and self.record["images"] is not u"" and self.record["images"] is not "":
            self.images = self.record["images"].split(",")

    def post(self, *args):
        record_id = self.params.get_string("id")
        category = self.params.get_string("category")
        category_record = self.sql.query_by_id("ProductCategory", category)

        self.sql.update("Product", {
            "product_name": self.params.get_string("product_name"),
            "product_no": self.params.get_string("product_no"),
            "content": self.params.get_string("content"),
            "parent_category": category_record["parent"],
            "price": self.params.get_string("price"),
            "images": ",".join(self.params.get_list("images")),
            "image": self.params.get_string("image"),
            "category": category,
        }, {
            "id": record_id
        })
        self.json({"info": u'產品已更新', "content": u"您已經成功的變更了此筆產品。"})