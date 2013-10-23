#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Freighttype(
  title       varchar(255),
  content     mediumtext,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;


create table Freight(
  title       varchar(255),
  start       float,
  end         float,
  amount      float,
  category    int,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;
        record.start       = start
        record.amount      = amount
        record.end         = end
        record.category    = category_key
"""


class full_list(AdministratorHandler):
    def get(self, *args):
        self.results = []
        list = self.sql.query_all('SELECT * FROM Freighttype ORDER BY sort desc')
        for item in list:
            self.results.append(item)
            sub_list = self.sql.query_all("SELECT * FROM Freight WHERE category = %s ORDER BY sort desc", item["id"])
            for sub_item in sub_list:
                sub_item["is_not_root"] = True
                self.results.append(sub_item)


class type_list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Freighttype', (), size)
        self.results = self.sql.query_all('SELECT * FROM Freighttype ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)

        self.render("/admin/freight/type_list.html")

class type_create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today()
        self.render("/admin/freight/type_create.html")

    def post(self, *args):
        self.sql.insert("Freighttype", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
            "is_enable": '1',
        })
        self.json({"info": u'付款方式已新增', "content": u"您已經成功的新增了一筆付款方式。"})


class type_edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Freighttype where id = %s', id)
        self.render("/admin/freight/type_edit.html")

    def post(self, *args):
        self.sql.update("Freighttype", {
            "title": self.request.get('title') if self.request.get('title') is not None else u'',
        }, {
            "id": self.request.get('id') if self.request.get('id') is not None else ''
        })
        self.json({"info": u'付款方式已更新', "content": u"您已經成功的變更了此筆付款方式。"})


class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Freight', (), size)
        self.results = self.sql.query_all('SELECT * FROM Freight ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)
        self.render("/admin/freight/list.html")

class create(AdministratorHandler):
    def get(self, *args):
        self.results = self.sql.query_all('SELECT * FROM Freighttype ORDER BY sort desc')
        self.render("/admin/freight/create.html")

    def post(self, *args):
        try:
            start = float(self.request.get('start')) if self.request.get('start') is not None else -1.0
        except:
            self.json({"info": u'新增失敗', "content": u"起始值必需為數字"})
            return
        try:
            end = float(self.request.get('end')) if self.request.get('end') is not None else -1.0
        except:
            self.json({"info": u'新增失敗', "content": u"結束值必需為數字"})
            return
        try:
            amount = float(self.request.get('amount')) if self.request.get('amount') is not None else 0.0
        except:
            self.json({"info": u'更新失敗', "content": u"金額必需為數字"})

        if start < 0:
            self.json({"info": u'新增失敗', "content": u"起始值必需大於 0"})
            return
        if start > end:
            self.json({"info": u'新增失敗', "content": u"結束值必需大於起始值"})
            return

        try:
            category = self.request.get('category') if self.request.get('category') is not None else u''
            type_record = self.sql.query_one('SELECT * FROM Freighttype where id = %s', category)
            if type_record is None:
                self.json({"info": u'更新失敗', "content": u"運費類別不存在"})
                return
        except:
            self.json({"info": u'新增失敗', "content": u"運費類別不存在"})
            return

        list = self.sql.query_all("SELECT * FROM Freight WHERE category = %s ORDER BY sort desc", int(category))
        for i in list:
            if (i["start"]-0.00001) < start < (i["end"]+0.00001):
                self.json({"info": u'新增失敗', "content": u"起始值包含在其它範圍中"})
                return
            if (i["start"]-0.00001) < end < (i["end"]+0.00001):
                self.json({"info": u'新增失敗', "content": u"結束值包含在其它範圍中"})
                return
            if start < i["start"] and end > i["end"]:
                self.json({"info": u'新增失敗', "content": u"不可涵蓋其它範圍"})
                return

        title = u"從 " + str(start) + u" 至 " + str(end) + u" 的運費為 " + str(amount)
        if self.is_localhost:
            title = u"From " + str(start) + u" To " + str(end) + u" Freight is " + str(amount)
        self.sql.insert("Freight", {
            "start": start,
            "end": end,
            "amount": amount,
            "category": category,
            "title": title
        })
        self.json({"info": u'運費設定已新增', "content": u"您已經成功的新增了一筆運費設定。"})

class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Freight where id = %s', id)
        self.results = self.sql.query_all('SELECT * FROM Freighttype ORDER BY sort desc')
        for item in self.results:
            item["is_select"] = (self.record["category"] == item["id"])
        self.render("/admin/freight/edit.html")

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        record = self.sql.query_one('SELECT * FROM Freight where id = %s', id)
        if record is not None:
            try:
                start = float(self.request.get('start')) if self.request.get('start') is not None else -1.0
            except:
                self.json({"info": u'更新失敗', "content": u"起始值必需為數字"})
                return
            try:
                end = float(self.request.get('end')) if self.request.get('end') is not None else -1.0
            except:
                self.json({"info": u'更新失敗', "content": u"結束值必需為數字"})
            try:
                amount = float(self.request.get('amount')) if self.request.get('amount') is not None else 0.0
            except:
                self.json({"info": u'更新失敗', "content": u"金額必需為數字"})
                return
            if start < 0:
                self.json({"info": u'更新失敗', "content": u"起始值必需大於 0"})
                return
            if start > end:
                self.json({"info": u'更新失敗', "content": u"結束值必需大於起始值"})
                return

            category = self.request.get('category') if self.request.get('category') is not None else u''
            type_record = self.sql.query_one('SELECT * FROM Freighttype where id = %s', category)
            if type_record is None:
                self.json({"info": u'更新失敗', "content": u"運費類別不存在"})
                return

            list = self.sql.query_all("SELECT * FROM Freight WHERE category = %s ORDER BY sort desc", int(category))
            for i in list:
                if (i["start"]-0.00001) < start < (i["end"]+0.00001) and (i["id"] != record["id"]):
                    self.json({"info": u'更新失敗', "content": u"起始值包含在其它範圍中"})
                    return
                if (i["start"]-0.00001) < end < (i["end"]+0.00001) and (i["id"] != record["id"]):
                    self.json({"info": u'更新失敗', "content": u"結束值包含在其它範圍中"})
                    return
                if start < i["start"] and end > i["end"] and (i["id"] != record["id"]):
                    self.json({"info": u'更新失敗', "content": u"不可涵蓋其它範圍"})
                    return
            title = u"從 " + str(start) + u" 至 " + str(end) + u" 的運費為 " + str(amount)
            if self.is_localhost:
                title = u"From " + str(start) + u" To " + str(end) + u" Freight is " + str(amount)

            self.sql.update("Freight", {
                "start": start,
                "end": end,
                "amount": amount,
                "category": category,
                "title": title
            }, {
                "id": id
            })
            self.json({"info": u'運費設定已更新', "content": u"您已經成功的更新了此筆運費設定。"})
        else:
            self.json({"info": u'無法更新', "content": u"此記錄已不存在。"})