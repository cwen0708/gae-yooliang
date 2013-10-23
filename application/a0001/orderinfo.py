#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table OrderInfo(
  order_no       varchar(100),
  title          varchar(500),
  items_total    float,
  items_count    int,
  freight        float,
  discount       float,
  total_amount   float,
  member_id      int not null,
  purchaser_name      varchar(500),
  purchaser_email     varchar(500),
  purchaser_mobile    varchar(500),
  purchaser_telephone varchar(500),
  purchaser_address_county  varchar(255),
  purchaser_address_area    varchar(255),
  purchaser_address_zip     varchar(10),
  purchaser_address_detail  varchar(500),
  recipient_name      varchar(500),
  recipient_email     varchar(500),
  recipient_mobile    varchar(500),
  recipient_telephone varchar(500),
  recipient_address_county  varchar(255),
  recipient_address_area    varchar(255),
  recipient_address_zip     varchar(10),
  recipient_address_detail  varchar(500),
  pay_type_id         int,
  pay_type            varchar(500),
  remark              text,
  order_status        int not null,
  pay_status          int not null,
  send_status         int not null,
  last_change         datetime,
  create_date varchar(25) NOT NULL,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;

create table OrderItem(
  product_id     int not null,
  product_no     varchar(500),
  product_name   varchar(500),
  product_price  float,
  product_image  text,
  product_url    varchar(500),
  item_quantity  int not null,
  item_status    int not null,
  item_sum       float,
  order_id       int not null,
  is_enable      tinyint(1),
  is_delete      tinyint(1) default 0,
  sort           timestamp default current_timestamp,
  id             int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;
"""


class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        str_order_status = self.request.get("order_status") if self.request.get("order_status") is not None and self.request.get("order_status") is not "" else u""
        str_pay_status = self.request.get("pay_status") if self.request.get("order_status") is not None and self.request.get("pay_status") is not "" else u""
        str_send_status = self.request.get("send_status") if self.request.get("send_status") is not None and self.request.get("send_status") is not "" else u""

        status = 0
        if str_order_status is not u"":
            status = int(str_order_status)
            self.page_all = self.sql.pager('SELECT count(1) FROM OrderInfo Where order_status = %s', status, size)
            self.results = self.sql.query_all('SELECT * FROM OrderInfo Where order_status = %s ORDER BY sort DESC LIMIT %s, %s', (status, (page - 1) * size, size), (page - 1) * size)
        if str_pay_status is not u"":
            status = int(str_pay_status)
            self.page_all = self.sql.pager('SELECT count(1) FROM OrderInfo Where order_status = %s', status, size)
            self.results = self.sql.query_all('SELECT * FROM OrderInfo Where order_status > 0 and pay_status = %s ORDER BY sort DESC LIMIT %s, %s', (status, (page - 1) * size, size), (page - 1) * size)
        if str_send_status is not u"":
            status = int(str_send_status)
            self.page_all = self.sql.pager('SELECT count(1) FROM OrderInfo Where order_status = %s', status, size)
            self.results = self.sql.query_all('SELECT * FROM OrderInfo Where order_status > 0 and send_status = %s ORDER BY sort DESC LIMIT %s, %s', (status, (page - 1) * size, size), (page - 1) * size)


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
        self.json({"info": u'訂單資訊已新增', "content": u"您已經成功的新增了一筆訂單資訊。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', id)
            self.member = self.sql.query_one('SELECT * FROM Member where id = %s', self.record["member_id"])
            self.item_list = self.sql.query_all('SELECT * FROM OrderItem where order_id = %s', id)
            self.total = int(self.record["total_amount"] + self.record["freight"])

    def post(self, *args):
        pay_status = self.params.get_integer("pay_status")
        send_status = self.params.get_integer("send_status")
        order_status = 2
        if pay_status == 0 and send_status == 0:
            order_status = 1
        if pay_status ==3 and send_status == 4:
            order_status = 3
        self.sql.update("OrderInfo", {
            "pay_status": pay_status,
            "send_status": send_status,
            "order_status": order_status,
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'訂單資訊已更新', "content": u"您已經成功的變更了此筆訂單資訊。"})


