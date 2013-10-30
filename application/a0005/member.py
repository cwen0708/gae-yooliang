#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler

SQL_All_MEMBER_COUNT = "SELECT count(1) FROM Member"
SQL_SELECT_ALL_BY_PAGE = "SELECT id, user_name, is_enable, is_delete, sort FROM Member ORDER BY sort DESC LIMIT %s, %s"

class Init(AdministratorHandler):
    def get(self, *args):
        self.sql.query_one(
            """
            create table Member(
              user_account    varchar(255),
              user_password   varchar(255),
              user_name       varchar(255),
              birthday        varchar(50),
              telephone       varchar(255),
              mobile          varchar(255),
              address_county  varchar(255),
              address_area    varchar(255),
              address_zip     varchar(10),
              address_detail  text,
              email           text,
              remark          text,
              is_dealer       tinyint(1),
              is_custom_account   tinyint(1),
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
        self.page_all = self.sql.pager(SQL_All_MEMBER_COUNT, (), size)
        self.results = self.sql.query_all(SQL_SELECT_ALL_BY_PAGE, ((page - 1) * size, size), (page - 1) * size)


class Create(AdministratorHandler):
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

        self.sql.insert('Member', {
            "user_account": self.params.get_string("user_account"),
            "user_password": self.params.get_string("user_password"),
            "user_name": self.params.get_string("user_name"),
            "birthday_year": self.params.get_string("birthday_year"),
            "birthday_month": self.params.get_string("birthday_month"),
            "birthday_day": self.params.get_string("birthday_day"),
            "telephone": self.params.get_string("telephone"),
            "mobile": self.params.get_string("mobile"),
            "address": self.params.get_string("address"),
            "email": self.params.get_string("email"),
            "remark": self.params.get_string("remark"),
            "is_dealer": self.params.get_integer("is_dealer"),
            "is_enable": 1,
            "is_custom_account": 0,
        })
        self.json({"info": u'會員資料已新增', "content": u"您已經成功的新增了一筆會員資料。"})


class edit(AdministratorHandler):
    def get(self, *args):
        user_id = self.params.get_string("id")
        if user_id != '':
            self.record = self.sql.query_one('SELECT * FROM Member where id = %s', user_id)

    def post(self, *args):
        user_id = self.params.get_string("id")
        user_account = self.params.get_string("user_account")
        email = self.params.get_string("email")

        if self.sql.query_one('SELECT * FROM Member where email = %s and id != %s', (email, user_id)) is not None:
            self.json({"info": u'會員資料更新失敗', "content": u"此信箱已被使用，請換一個。"})
            return

        if self.sql.query_one('SELECT * FROM Member where user_account = %s and id != %s', (user_account, user_id)) is not None:
            self.json({"info": u'會員資料更新失敗', "content": u"此帳號已被使用，請換一個。"})
            return

        self.sql.update('Member',{
            "user_account": user_account,
            "user_password": self.params.get_string("user_password"),
            "user_name": self.params.get_string("user_name"),
            "birthday_year": self.params.get_string("birthday_year"),
            "birthday_month": self.params.get_string("birthday_month"),
            "birthday_day": self.params.get_string("birthday_day"),
            "telephone": self.params.get_string("telephone"),
            "mobile": self.params.get_string("mobile"),
            "address": self.params.get_string("address"),
            "email": self.params.get_string("email"),
            "remark": self.params.get_string("remark"),
        },{
            "id": user_id
        })
        self.json({"info": u'會員資料已更新', "content": u"您已經成功的變更了此筆會員資料。"})