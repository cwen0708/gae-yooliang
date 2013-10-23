#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table RawData(
  customer_id   int not null,
  case_id       int not null,
  kwh           float default 0,
  date          varchar(255),
  is_delete     tinyint(1) default 0,
  create_date   timestamp default 0,
  sort          timestamp,
  id            int not null auto_increment,
  primary key   (id)
) engine=myisam default charset=utf8;

create table StatisticsData(
  customer_id   int not null,
  case_id       int not null,
  date          varchar(255),
  kwh           float default 0,
  last_kwh      float default 0,
  is_delete   tinyint(1) default 0,
  sort        timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;

drop table StatisticsData ;
alter table StatisticsData add last_kwh float default 0 after kwh;
alter table RawData drop column equipment_id;
alter table StatisticsData drop column equipment_id;
"""

class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM RawData', (), size)
        self.results = self.sql.query_all('SELECT * FROM RawData ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)

        for item in self.results:
            customer_record = self.sql.query_one('SELECT * FROM Customer where id = %s', item["customer_id"])
            case_record = self.sql.query_one('SELECT * FROM CaseInfo where id = %s', item["case_id"])
            item["customer_name"] = customer_record["customer_name"]
            item["case_name"] = case_record["case_name"]


class create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        customer_name = self.request.get('customer_name') if self.request.get('customer_name') is not None else u''
        customer_no = self.request.get('customer_no') if self.request.get('customer_no') is not None else u''
        account = self.request.get('account') if self.request.get('account') is not None else u''
        password = self.request.get('password') if self.request.get('password') is not None else u''

        self.sql.cursor.execute('SELECT * FROM Customer where account = %s', account)
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'客戶帳號新增失敗', "content": u"此帳號已有人使用，請換一個。"})
            return

        self.sql.cursor.execute('INSERT INTO Customer (customer_name,customer_no, account, password, is_enable) VALUES (%s, %s, %s, %s)', (customer_name, customer_no, account, password, '1'))

        self.json({"info": u'客戶資料已新增', "content": u"您已經成功的新增了一筆客戶資料。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, customer_name, customer_no, account, password,  is_enable FROM Customer where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "customer_name": record[1],
                "customer_no": record[2],
                "account": record[3],
                "password": record[4],
                "is_enable": (record[5] == 1)
            }

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        customer_name = self.request.get('customer_name') if self.request.get('customer_name') is not None else u''
        customer_no = self.request.get('customer_no') if self.request.get('customer_no') is not None else u''
        account = self.request.get('account') if self.request.get('account') is not None else u''
        password = self.request.get('password') if self.request.get('password') is not None else u''

        self.sql.cursor.execute('SELECT * FROM Customer where account = %s and id != %s', (account, id))
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'客戶帳號更新失敗', "content": u"此帳號已有人使用，請換一個。"})
            return

        self.sql.cursor.execute('SELECT * FROM Customer where customer_no = %s and id != %s', (customer_no, id))
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'客戶帳號更新失敗', "content": u"此編號已有人使用，請換一個。"})
            return

        self.sql.cursor.execute('SELECT id FROM Customer where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'客戶資料更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE Customer SET customer_name = %s, account = %s, password = %s where id = %s', (customer_name, account, password, id))
            self.json({"info": u'客戶資料已更新', "content": u"您已經成功的變更了此筆客戶資料。"})