#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Solution(
  title       varchar(255),
  content     mediumtext,
  image       varchar(2000) NOT NULL,
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
        self.page_all = self.sql.pager('SELECT count(1) FROM Solution', (), size)
        self.results = self.sql.query_all('SELECT * FROM Solution ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        full_content = self.request.get('full_content') if self.request.get('full_content') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''

        self.sql.cursor.execute('INSERT INTO Solution (title, content, full_content, image, is_enable) VALUES (%s, %s, %s, %s, %s)', (title, content, full_content, image, '1'))
        self.json({"info": u'系統套案已新增', "content": u"您已經成功的新增了一筆系統套案。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, title, content, image,  is_enable FROM Solution where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "image": record[3],
                "is_enable": (record[4] == 1)
            }

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        content = self.request.get('content') if self.request.get('content') is not None else u''
        full_content = self.request.get('full_content') if self.request.get('full_content') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''
        id = self.request.get('id') if self.request.get('id') is not None else ''

        self.sql.cursor.execute('SELECT id FROM Solution where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'系統套案更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE Solution SET title = %s, content = %s, full_content = %s, image = %s where id = %s', (title, content, full_content, image, id))
            self.json({"info": u'系統套案已更新', "content": u"您已經成功的變更了此筆系統套案。"})
