#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table CaseInfo(
  case_id       varchar(500),
  case_name     varchar(500),
  case_no       varchar(500),
  image         varchar(2000),
  place         varchar(500),
  price         float,
  max_kw        float,
  kw            float,
  start_kwh     float,
  type_image    text,
  address       varchar(500),
  system_type   varchar(500),
  complete_date varchar(500),
  is_enable     tinyint(1),
  is_delete     tinyint(1) default 0,
  sort          timestamp default current_timestamp,
  customer_id   int not null,
  id            int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;

alter table CaseInfo add woeid varchar(500) after kw;
alter table CaseInfo add price float after place;
"""

class List(AdministratorHandler):
    def get(self, *args):
        cid = self.params.get_string("cid")
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.host_str = str(self.environ.host)
        try:
            the_cid = int(cid)
            self.page_all = self.sql.pager("SELECT count(1) FROM CaseInfo WHERE customer_id = %s ORDER BY sort", the_cid, size)
            self.results = self.sql.query_all('SELECT *, case_name as title FROM CaseInfo WHERE customer_id = %s ORDER BY sort DESC LIMIT %s, %s', (the_cid, (page - 1) * size, size))
        except:
            self.page_all = self.sql.pager('SELECT count(1) FROM CaseInfo', (), size)
            self.results = self.sql.query_all('SELECT *, case_name as title FROM CaseInfo ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))

        for item in self.results:
            customer_record = self.sql.query_one('SELECT customer_no FROM Customer where id = %s', item["customer_id"])
            item["customer_no"] = customer_record["customer_no"]

class create(AdministratorHandler):
    def get(self, *args):
        cid = self.params.get_string("cid")
        customer_record = self.sql.query_one('SELECT customer_name FROM Customer where id = %s', cid)
        self.customer_name = customer_record["customer_name"]

    def post(self, *args):
        cid = self.params.get_string("cid")
        case_id = self.params.get_string("cid") + "-" + self.params.get_string("case_no")
        record = self.sql.query_one('SELECT * FROM CaseInfo where case_id = %s', case_id)
        if record is not None:
            self.json({"info": u'案場資料新增失敗', "content": u"此客戶已有相同編號的案場，請換一個。"})
            return
        self.sql.insert("CaseInfo", {
            "case_id": case_id,
            "case_name": self.params.get_string("case_name"),
            "case_no": self.params.get_string("case_no"),
            "place": self.params.get_string("place"),
            "price":  self.params.get_float('price', 0.0),
            "max_kw": self.params.get_float('max_kw', 0.0),
            "start_kwh": self.params.get_float('start_kwh', 0.0),
            "address": self.params.get_string("address"),
            "system_type": self.params.get_string("system_type"),
            "complete_date": self.params.get_string("complete_date"),
            "type_image": self.params.get_string("type_image"),
            "image": self.params.get_string("image"),
            "image2": self.params.get_string("image2"),
            "info": self.params.get_string("info"),
            "images": ",".join(self.params.get_list("images")),
            "woeid": self.params.get_string("woeid"),
            "is_enable": 1,
            "customer_id": cid,
        })
        self.json({"info": u'案場資料已新增', "content": u"您已經成功的新增了一筆案場資料。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM CaseInfo where id = %s', id)
            customer_record = self.sql.query_one('SELECT customer_name FROM Customer where id = %s', self.record["customer_id"])
            self.record["customer_name"] = customer_record["customer_name"]
            if self.record["images"] is not None and self.record["images"] is not u"" and self.record["images"] is not "":
                self.images = self.record["images"].split(",")

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        case_no = self.request.get('case_no') if self.request.get('case_no') is not None else u''

        old_record = self.sql.query_one('SELECT customer_id FROM CaseInfo where id = %s', id)
        case_id = str(old_record["customer_id"]) + "-" + case_no

        check_record = self.sql.query_one('SELECT * FROM CaseInfo where case_id = %s And id != %s', (case_id, id))
        if check_record is not None:
            self.json({"info": u'案場資料新增失敗', "content": u"此客戶已有相同編號的案場，請換一個。"})
            return

        self.sql.update("CaseInfo", {
            "case_id": case_id,
            "case_name": self.params.get_string("case_name"),
            "case_no": self.params.get_string("case_no"),
            "place": self.params.get_string("place"),
            "price":  self.params.get_float('price', 0.0),
            "max_kw": self.params.get_float('max_kw', 0.0),
            "start_kwh": self.params.get_float('start_kwh', 0.0),
            "address": self.params.get_string("address"),
            "system_type": self.params.get_string("system_type"),
            "complete_date": self.params.get_string("complete_date"),
            "type_image": self.params.get_string("type_image"),
            "image": self.params.get_string("image"),
            "image2": self.params.get_string("image2"),
            "info": self.params.get_string("info"),
            "images": ",".join(self.params.get_list("images")),
            "woeid": self.params.get_string("woeid"),
        }, {
            "id": self.params.get_string("id")
        })

        self.json({"info": u'案場資料已更新', "content": u"您已經成功的變更了此筆案場資料。"})