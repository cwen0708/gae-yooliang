#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Marquee(
  title       varchar(255),
  content     mediumtext,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Marquee', (), size)
        self.results = self.sql.query_all('SELECT * FROM Marquee ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        import datetime
        self.today = datetime.datetime.today()

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''

        self.sql.cursor.execute('INSERT INTO Marquee (title, content, is_enable) VALUES (%s, %s, %s)', (title, content, '1'))

        self.json({"info": u'跑馬燈已新增', "content": u"您已經成功的新增了一筆跑馬燈。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, title, content, is_enable FROM Marquee where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "is_enable": (record[3] == 1)
            }

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        id = self.request.get('id') if self.request.get('id') is not None else ''

        self.sql.cursor.execute('SELECT id FROM Marquee where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'跑馬燈更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE Marquee SET title = %s, content = %s where id = %s', (title, content, id))
            self.json({"info": u'跑馬燈已更新', "content": u"您已經成功的變更了此筆跑馬燈。"})