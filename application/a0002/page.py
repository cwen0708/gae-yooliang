#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db

from application.backend.handler import AdministratorHandler
from libs.gaesite.database import *


class DBPage(DBBase):
    """ 產品分類 """
    title = db.StringProperty()
    content = db.TextProperty()
    name = db.StringProperty()

class list(AdministratorHandler):
    def get(self):
        data_source = db.GqlQuery("SELECT * FROM DBPage ORDER BY sort desc")
        self.results = data_source.fetch(self.size, (self.page - 1) * self.size)
        self.page_all = Pagination.get_all_page(self.results, "all", self.page, self.size)
        if self.page_all == 0:
            self.page_all = 1
        self.render("/admin/page/list.html")

class create(AdministratorHandler):
    def get(self):
        self.time_sp = int(time.time())
        self.render("/admin/page/create.html")

    def post(self):
        title = self.request.get('title') if self.request.get('title') is not None else u'未命名'
        content = self.request.get('content') if self.request.get('content') is not None else u'內容尚未編寫'

        record = DBPage()
        record.title = title
        record.content = content
        record.save()
        Pagination.add(record, record.is_enable)
        self.json({"info": u'頁面內容已新增', "content": u"您已經成功的新增了一筆頁面內容。"})

class edit(AdministratorHandler):
    def get(self):
        record = None
        key = self.request.get('key') if self.request.get('key') is not None else u''
        if key is not u"" and key is not "":
            record = db.get(key)
        if record is None:
            name = self.request.get('name') if self.request.get('name') is not None else u''
            if name is not u"":
                record = db.GqlQuery("SELECT * FROM DBPage WHERE name = :1", name).get()
                if record is None:
                    record = DBPage()
                    record.name = name
                    record.can_delete = False
                    record.title = name
                record.save()
        self.record = record
        self.render("/admin/page/edit.html")

    def post(self):
        record = db.get(self.request.get('key'))
        if record is not None:
            record.title = self.request.get('title') if  self.request.get('title') is not None else u'未命名'
            record.content = self.request.get('content') if self.request.get('content') is not None else u'內容尚未編寫'
            record.save()
            self.json({"info": u'頁面已更新', "content": u"您已經成功的變更了此筆頁面。"})
        else:
            self.json({"info": u'無法更新', "content": u"此記錄已不存在。"})