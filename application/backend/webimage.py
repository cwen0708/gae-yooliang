#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26

from application.backend.handler import AdministratorHandler
"""
create table WebImage(
  setting_name  varchar(255),
  setting_no    varchar(255),
  value         text,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM WebImage', (), size)
        self.results = self.sql.query_all('SELECT * FROM WebImage ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        for item in self.results:
            item["title"] = item["setting_name"]
        self.render("/v1/webimage/list.html", "backend")


class create(AdministratorHandler):
    def get(self, *args):
        self.render("/v1/webimage/create.html", "backend")

    def post(self, *args):
        setting_name = self.request.get('setting_name') if self.request.get('setting_name') is not None else u''
        setting_no = self.request.get('setting_no') if self.request.get('setting_no') is not None else u''
        value = self.request.get('value') if self.request.get('value') is not None else u''

        if self.sql.query_one('SELECT * FROM WebImage where setting_no = %s', setting_no) is not None:
            self.json({"info": u'網站圖片新增失敗', "content": u"此編號已有被使用，請換一個。"})
            return

        self.sql.insert("WebImage", {
            "setting_name": setting_name,
            "setting_no": setting_no,
            "value": value,
        })
        self.json({"info": u'網站圖片已新增', "content": u"您已經成功的新增了一筆網站圖片。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM WebImage where id = %s', id)
        self.render("/v1/webimage/edit.html", "backend")

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        setting_name = self.request.get('setting_name') if self.request.get('setting_name') is not None else u''
        setting_no = self.request.get('setting_no') if self.request.get('setting_no') is not None else u''
        value = self.request.get('value') if self.request.get('value') is not None else u''

        if self.sql.query_one('SELECT * FROM WebImage where setting_no = %s and id != %s', (setting_no, id)) is not None:
            self.json({"info": u'網站圖片更新失敗', "content": u"此編號已有被使用，請換一個。"})
            return

        self.sql.update("WebImage", {
            "setting_name": setting_name,
            "setting_no": setting_no,
            "value": value,
        }, {
            "id": id
        })
        self.json({"info": u'網站圖片已更新', "content": u"您已經成功的變更了此筆網站圖片。"})