#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table News(
  title       varchar(255),
  content     mediumtext,
  create_date varchar(2000) NOT NULL,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM News', (), size)
        self.results = self.sql.query_all('SELECT * FROM News ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today()

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        create_date = self.request.get('create_date') if self.request.get('create_date') is not None else u''

        self.sql.cursor.execute('INSERT INTO News (title, content, create_date, is_enable) VALUES (%s, %s, %s, %s)', (title, content, create_date, '1'))

        self.json({"info": u'最新消息已新增', "content": u"您已經成功的新增了一筆最新消息。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, title, content, create_date,  is_enable FROM News where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "create_date": record[3],
                "is_enable": (record[4] == 1)
            }

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        create_date = self.request.get('create_date') if self.request.get('create_date') is not None else u''
        id = self.request.get('id') if self.request.get('id') is not None else ''

        self.sql.cursor.execute('SELECT id FROM News where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'最新消息更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE News SET title = %s, content = %s, create_date = %s where id = %s', (title, content, create_date, id))
            self.json({"info": u'最新消息已更新', "content": u"您已經成功的變更了此筆最新消息。"})