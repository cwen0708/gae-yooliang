#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table WebSetting(
  setting_name  varchar(255),
  setting_no    varchar(255),
  value         varchar(255),
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

        self.sql.cursor.execute('SELECT count(1) FROM WebSetting')
        results = self.sql.cursor.fetchone()
        self.page_now = page
        self.page_all = self.get_page_count(results[0], size)

        self.sql.cursor.execute('SELECT id, setting_name, value, is_enable, is_delete, sort FROM WebSetting ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        self.rowcount = self.sql.cursor.rowcount
        results = self.sql.cursor.fetchall()
        row_id = (page - 1) * size
        self.results = []
        for item in results:
            row_id += 1
            item_temp = {
                "row_id": row_id,
                "id": item[0],
                "title": item[1] + " " + item[2],
                "is_enable": (item[3] == 1),
                "is_delete": (item[4] == 1),
                "sort": item[5]
            }
            self.results.append(item_temp)


class create(AdministratorHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        setting_name = self.request.get('setting_name') if self.request.get('setting_name') is not None else u''
        setting_no = self.request.get('setting_no') if self.request.get('setting_no') is not None else u''
        value = self.request.get('value') if self.request.get('value') is not None else u''

        self.sql.cursor.execute('SELECT * FROM WebSetting where setting_no = %s', setting_no)
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'網站設定新增失敗', "content": u"此編號已有被使用，請換一個。"})
            return

        self.sql.cursor.execute('INSERT INTO WebSetting (setting_name, setting_no, value, is_enable) VALUES (%s, %s, %s, %s)', (setting_name, setting_no, value, '1'))

        self.json({"info": u'網站設定已新增', "content": u"您已經成功的新增了一筆網站設定。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, setting_name, setting_no, value, is_enable FROM WebSetting where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "setting_name": record[1],
                "setting_no": record[2],
                "value": record[3],
                "is_enable": (record[4] == 1)
            }

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        setting_name = self.request.get('setting_name') if self.request.get('setting_name') is not None else u''
        setting_no = self.request.get('setting_no') if self.request.get('setting_no') is not None else u''
        value = self.request.get('value') if self.request.get('value') is not None else u''

        self.sql.cursor.execute('SELECT * FROM WebSetting where setting_no = %s and id != %s', (setting_no, id))
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'網站設定更新失敗', "content": u"此編號已有被使用，請換一個。"})
            return

        self.sql.cursor.execute('SELECT id FROM WebSetting where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'網站設定更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE WebSetting SET setting_name = %s, setting_no = %s, value = %s where id = %s', (setting_name, setting_no, value, id))
            self.json({"info": u'網站設定已更新', "content": u"您已經成功的變更了此筆網站設定。"})