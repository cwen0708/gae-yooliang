#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table StatusCode(
  title  varchar(2000),
  status_code_no    varchar(255),
  report_time       int,
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

        self.sql.cursor.execute('SELECT count(1) FROM StatusCode')
        results = self.sql.cursor.fetchone()
        self.page_now = page
        self.page_all = self.get_page_count(results[0], size)

        self.sql.cursor.execute('SELECT id, title, report_time, is_enable, is_delete, sort FROM StatusCode ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        self.rowcount = self.sql.cursor.rowcount
        results = self.sql.cursor.fetchall()
        row_id = (page - 1) * size
        self.results = []
        for item in results:
            row_id += 1
            item_temp = {
                "row_id": row_id,
                "id": item[0],
                "title": item[1],
                "is_enable": (item[3] == 1),
                "is_delete": (item[4] == 1),
                "sort": item[5]
            }
            self.results.append(item_temp)


class create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        title = self.request.get('title') if self.request.get('title') is not None else u''
        status_code_no = self.request.get('status_code_no') if self.request.get('status_code_no') is not None else u''
        report_time = int(self.request.get('report_time')) if self.request.get('report_time') is not None else 0

        self.sql.cursor.execute('SELECT * FROM StatusCode where status_code_no = %s', status_code_no)
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'訊息代碼新增失敗', "content": u"此編號已有被使用，請換一個。"})
            return

        self.sql.cursor.execute('INSERT INTO StatusCode (title, status_code_no, report_time, is_enable) VALUES (%s, %s, %s, %s)', (title, status_code_no, report_time, '1'))

        self.json({"info": u'訊息代碼已新增', "content": u"您已經成功的新增了一筆訊息代碼。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, title, status_code_no, report_time, is_enable FROM StatusCode where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "title": record[1],
                "status_code_no": record[2],
                "report_time": record[3],
                "is_enable": (record[4] == 1)
            }

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        title = self.request.get('title') if self.request.get('title') is not None else u''
        status_code_no = self.request.get('status_code_no') if self.request.get('status_code_no') is not None else u''
        report_time = int(self.request.get('report_time')) if self.request.get('report_time') is not None else 0

        self.sql.cursor.execute('SELECT * FROM StatusCode where status_code_no = %s and id != %s', (status_code_no, id))
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'訊息代碼更新失敗', "content": u"此編號已有被使用，請換一個。"})
            return

        self.sql.cursor.execute('SELECT id FROM StatusCode where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'訊息代碼更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE StatusCode SET title = %s, status_code_no = %s, report_time = %s where id = %s', (title, status_code_no, report_time, id))
            self.json({"info": u'訊息代碼已更新', "content": u"您已經成功的變更了此筆訊息代碼。"})