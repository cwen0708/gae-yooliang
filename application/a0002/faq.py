#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Faq(
  title       varchar(500),
  content     mediumtext,
  category    int not null,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  create_date varchar(2000),
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;

create table FaqCategory(
  category_name    varchar(255),
  parent           int not null,
  is_enable   tinyint(1),
  is_delete   tinyint(1) default 0,
  sort        timestamp default current_timestamp,
  id          int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;
"""



class category_list(AdministratorHandler):
    def get(self, *args):
        self.sql.cursor.execute('SELECT id, category_name, is_enable, is_delete, sort FROM FaqCategory Where parent = 0 ORDER BY sort DESC')
        self.results = []
        for item in self.sql.cursor.fetchall():
            self.sql.cursor.execute('SELECT id, category_name, is_enable, is_delete, sort FROM FaqCategory Where parent = %s ORDER BY sort DESC', item[0])
            temp_list = self.sql.cursor.fetchall()
            item_temp = {
                "id": item[0],
                "category_name": item[1],
                "is_enable": (item[2] == 1),
                "is_delete": (item[3] == 1),
                "sort": item[4],
                "is_not_root": False
            }
            self.results.append(item_temp)
            for item_sub in temp_list:
                item_temp = {
                    "id": item_sub[0],
                    "category_name": item_sub[1],
                    "is_enable": (item_sub[2] == 1),
                    "is_delete": (item_sub[3] == 1),
                    "sort": item_sub[4],
                    "is_not_root": True
                }
                self.results.append(item_temp)


class category_create(AdministratorHandler):
    def get(self, *args):
        self.sql.cursor.execute('SELECT id, category_name, is_enable, is_delete, sort FROM FaqCategory Where parent = 0 ORDER BY sort DESC')
        self.results = []
        for item in self.sql.cursor.fetchall():
            item_temp = {
                "id": item[0],
                "category_name": item[1],
                "is_enable": (item[2] == 1),
                "is_delete": (item[3] == 1),
                "sort": item[4]
            }
            self.results.append(item_temp)

    def post(self, *args):
        category_name = self.request.get('title') if self.request.get('title') is not None else u''
        parent = self.request.get('parent') if self.request.get('parent') is not None else u''

        self.sql.cursor.execute('INSERT INTO FaqCategory (category_name, parent, is_enable) VALUES (%s, %s, %s)', (category_name, parent, '1'))

        self.json({"info": u'問與答分類已新增', "content": u"您已經成功的新增了一筆問與答分類。"})


class category_edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, category_name, parent, is_enable FROM FaqCategory where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "category_name": record[1],
                "parent": record[2],
                "is_enable": (record[3] == 1)
            }
        self.sql.cursor.execute('SELECT id, category_name, is_enable, is_delete, sort FROM FaqCategory Where parent = 0 ORDER BY sort DESC')
        self.results = []
        for item in self.sql.cursor.fetchall():
            item_temp = {
                "id": item[0],
                "category_name": item[1],
                "is_enable": (item[2] == 1),
                "is_delete": (item[3] == 1),
                "sort": item[4],
                "is_select": (self.record["parent"] == item[0])
            }
            self.results.append(item_temp)

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        category_name = self.request.get('title') if self.request.get('title') is not None else u''
        parent = self.request.get('parent') if self.request.get('parent') is not None else u''

        self.sql.cursor.execute('SELECT id FROM FaqCategory where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'問與答分類更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE FaqCategory SET category_name = %s, parent = %s where id = %s', (category_name, parent, id))
            self.json({"info": u'問與答分類已更新', "content": u"您已經成功的變更了此筆問與答分類。"})


class list(AdministratorHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        str_category = self.request.get("category") if self.request.get("category") is not None and self.request.get("category") is not "" else u""
        self.page_now = page

        if str_category is u"":
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq', (), size)
            self.results = self.sql.query_all('SELECT * FROM Faq ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)
        else:
            category = int(str_category)
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq Where category = %s', category, size)
            self.results = self.sql.query_all('SELECT * FROM Faq Where category = %s  ORDER BY sort DESC LIMIT %s, %s', (category, (page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today()
        self.sql.cursor.execute('SELECT id, category_name, is_enable, is_delete, sort FROM FaqCategory Where parent = 0 ORDER BY sort DESC')
        self.results = []
        for item in self.sql.cursor.fetchall():
            item_temp = {
                "id": item[0],
                "category_name": item[1],
                "is_enable": (item[2] == 1),
                "is_delete": (item[3] == 1),
                "sort": item[4]
            }
            self.results.append(item_temp)

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        create_date = self.request.get('create_date') if self.request.get('create_date') is not None else u''
        category = self.request.get('category') if self.request.get('category') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''

        self.sql.cursor.execute('INSERT INTO Faq (title, content, category, create_date, is_enable) VALUES (%s, %s, %s, %s, %s)', (title, content, int(category), create_date, '1'))
        self.json({"info": u'問與答已新增', "content": u"您已經成功的新增了一筆問與答。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, title, content, category, create_date, is_enable FROM Faq where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "category": record[3],
                "create_date": record[4],
                "is_enable": (record[5] == 1)
            }
        self.sql.cursor.execute('SELECT id, category_name, is_enable, is_delete, sort FROM FaqCategory Where parent = 0 ORDER BY sort DESC')
        self.results = []
        for item in self.sql.cursor.fetchall():
            item_temp = {
                "id": item[0],
                "category_name": item[1],
                "is_enable": (item[2] == 1),
                "is_delete": (item[3] == 1),
                "sort": item[4],
                "is_select": (self.record["category"] == item[0])
            }
            self.results.append(item_temp)

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        category = self.request.get('category') if self.request.get('category') is not None else u''
        create_date = self.request.get('create_date') if self.request.get('create_date') is not None else u''

        self.sql.cursor.execute('SELECT id FROM Faq where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'問與答更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE Faq SET title = %s, content = %s, category = %s, create_date =%s where id = %s', (title, content, int(category), create_date, id))
            self.json({"info": u'問與答已更新', "content": u"您已經成功的變更了此筆問與答。"})