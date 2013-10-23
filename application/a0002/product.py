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

class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Product', (), size)
        self.results = self.sql.query_all('SELECT * FROM Product ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
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
        category = self.request.get('category') if self.request.get('category') is not None else u''
        category_record = self.sql.query_one('SELECT * FROM ProductCategory where id = %s', category)
        image = self.request.get('image') if self.request.get('image') is not None else u''
        images = ",".join(self.params.get_list("images"))

        self.sql.insert("Product", {
            "product_name": self.request.get('product_name') if self.request.get('product_name') is not None else u'',
            "product_no": self.request.get('product_no') if self.request.get('product_no') is not None else u'',
            "original_price": self.request.get('original_price') if self.request.get('original_price') is not None else u'',
            "selling_price": self.request.get('selling_price') if self.request.get('selling_price') is not None else u'',
            "content": self.request.get('content') if self.request.get('content') is not None else u'',
            "category": category,
            "parent_category": category_record["parent"],
            "image": image,
            "images": images,
            "is_enable": '1',
        })
        self.json({"info": u'產品已新增', "content": u"您已經成功的新增了一筆產品。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Product where id = %s', id)

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

        if self.record["images"] is not None:
            self.images = self.record["images"].split(",")

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        category = self.request.get('category') if self.request.get('category') is not None else u''
        category_record = self.sql.query_by_id("ProductCategory", category)
        category_record = self.sql.query_one('SELECT * FROM ProductCategory where id = %s', category)
        image = self.request.get('image') if self.request.get('image') is not None else u''
        images = ",".join(self.params.get_list("images"))

        self.sql.update("Product", {
            "product_name": self.request.get('product_name') if self.request.get('product_name') is not None else u'',
            "product_no": self.request.get('product_no') if self.request.get('product_no') is not None else u'',
            "original_price": self.request.get('original_price') if self.request.get('original_price') is not None else u'',
            "selling_price": self.request.get('selling_price') if self.request.get('selling_price') is not None else u'',
            "content": self.request.get('content') if self.request.get('content') is not None else u'',
            "category": category,
            "parent_category": category_record["parent"],
            "image": image,
            "images": images,
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'產品已更新', "content": u"您已經成功的變更了此筆產品。"})