#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Member(
  user_account     varchar(255),
  user_password    varchar(255),
  user_name        varchar(255),
  birthday   varchar(50),
  telephone   varchar(255),
  mobile      varchar(255),
  address_county  varchar(255),
  address_area    varchar(255),
  address_zip     varchar(10),
  address_detail  text,
  email       varchar(255),
  remark      text,
  is_custom_account   tinyint(1),
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Member', (), size)
        self.results = self.sql.query_all('SELECT id, user_name, is_enable, is_delete, sort FROM Member ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today()

    def post(self, *args):
        user_account = self.request.get('user_account') if self.request.get('user_account') is not None else u''
        email = self.request.get('email') if self.request.get('email') is not None else u''

        if self.sql.query_one('SELECT * FROM Member where email = %s ', email) is not None:
            self.json({"info": u'會員資料新增失敗', "content": u"此信箱已被使用，請換一個。"})
            return

        if self.sql.query_one('SELECT * FROM Member where user_account = %s', user_account) is not None:
            self.json({"info": u'會員資料新增失敗', "content": u"此帳號已被使用，請換一個。"})
            return

        self.sql.insert('Member',{
            "user_account": self.request.get('user_account') if self.request.get('user_account') is not None else u'',
            "user_password": self.request.get('user_password') if self.request.get('user_password') is not None else u'',
            "user_name": self.request.get('user_name') if self.request.get('user_name') is not None else u'',
            "birthday_year": self.request.get('birthday_year') if self.request.get('birthday_year') is not None else u'',
            "birthday_month": self.request.get('birthday_month') if self.request.get('birthday_month') is not None else u'',
            "birthday_day": self.request.get('birthday_day') if self.request.get('birthday_day') is not None else u'',
            "telephone": self.request.get('telephone') if self.request.get('telephone') is not None else u'',
            "mobile": self.request.get('mobile') if self.request.get('mobile') is not None else u'',
            "address": self.request.get('address') if self.request.get('address') is not None else u'',
            "email": self.request.get('email') if self.request.get('email') is not None else u'',
            "remark": self.request.get('remark') if self.request.get('remark') is not None else u'',
            "is_enable": '1',
            "is_custom_account": '0',
        })
        self.json({"info": u'會員資料已新增', "content": u"您已經成功的新增了一筆會員資料。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Member where id = %s', id)

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''

        user_account = self.request.get('user_account') if self.request.get('user_account') is not None else u''
        user_password = self.request.get('user_password') if self.request.get('user_password') is not None else u''
        user_name = self.request.get('user_name') if self.request.get('user_name') is not None else u''
        birthday_year = self.request.get('birthday_year') if self.request.get('birthday_year') is not None else u''
        birthday_month = self.request.get('birthday_month') if self.request.get('birthday_month') is not None else u''
        birthday_day = self.request.get('birthday_day') if self.request.get('birthday_day') is not None else u''
        telephone = self.request.get('telephone') if self.request.get('telephone') is not None else u''
        mobile = self.request.get('mobile') if self.request.get('mobile') is not None else u''
        address = self.request.get('address') if self.request.get('address') is not None else u''
        email = self.request.get('email') if self.request.get('email') is not None else u''
        remark = self.request.get('remark') if self.request.get('remark') is not None else u''

        if self.sql.query_one('SELECT * FROM Member where email = %s and id != %s', (email, id)) is not None:
            self.json({"info": u'會員資料更新失敗', "content": u"此信箱已被使用，請換一個。"})
            return

        if self.sql.query_one('SELECT * FROM Member where user_account = %s and id != %s', (user_account, id)) is not None:
            self.json({"info": u'會員資料更新失敗', "content": u"此帳號已被使用，請換一個。"})
            return

        self.sql.update('Member',{
            "user_account": self.request.get('user_account') if self.request.get('user_account') is not None else u'',
            "user_password": self.request.get('user_password') if self.request.get('user_password') is not None else u'',
            "user_name": self.request.get('user_name') if self.request.get('user_name') is not None else u'',
            "birthday_year": self.request.get('birthday_year') if self.request.get('birthday_year') is not None else u'',
            "birthday_month": self.request.get('birthday_month') if self.request.get('birthday_month') is not None else u'',
            "birthday_day": self.request.get('birthday_day') if self.request.get('birthday_day') is not None else u'',
            "telephone": self.request.get('telephone') if self.request.get('telephone') is not None else u'',
            "mobile": self.request.get('mobile') if self.request.get('mobile') is not None else u'',
            "address": self.request.get('address') if self.request.get('address') is not None else u'',
            "email": self.request.get('email') if self.request.get('email') is not None else u'',
            "remark": self.request.get('remark') if self.request.get('remark') is not None else u'',
        },{
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'會員資料已更新', "content": u"您已經成功的變更了此筆會員資料。"})