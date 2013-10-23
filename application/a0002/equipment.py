#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
"""
create table Equipment(
  equipment_id       varchar(500),
  equipment_name     varchar(500),
  equipment_no       varchar(500),
  image         varchar(2000),
  is_enable     tinyint(1),
  is_delete     tinyint(1) default 0,
  status_code   varchar(2000),
  status_code_time   int,
  sort          timestamp default current_timestamp,
  last_update   timestamp,
  case_id       int not null,
  customer_id   int not null,
  id            int not null auto_increment,
  primary key (id)
) engine=myisam default charset=utf8;


SHOW COLUMNS FROM Equipment
drop table Equipment
alter table Equipment add status_code_time int not null default 0 after is_delete;
alter table Equipment drop column status_code;
alter table Equipment add status_code varchar(2000) after is_delete;
"""

class list(AdministratorHandler):
    def get(self, *args):
        cid = self.request.get('cid') if self.request.get('cid') is not None else u''
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        try:
            self.cid = int(cid)
            self.page_all = self.sql.pager('SELECT count(1) FROM Equipment WHERE case_id = %s ORDER BY sort', self.cid, size)
            self.results = self.sql.query_all('SELECT * FROM Equipment WHERE case_id = %s ORDER BY sort DESC LIMIT %s, %s', (self.cid, (page - 1) * size, size))
        except:
            self.page_all = self.sql.pager('SELECT count(1) FROM Equipment', {}, size)
            self.results = self.sql.query_all('SELECT * FROM Equipment ORDER BY sort  DESC LIMIT %s, %s', ((page - 1) * size, size))
        self.host_str = str(self.environ.host)

        for item in self.results:
            case_record = self.sql.query_one('SELECT case_no FROM CaseInfo where id = %s', item["case_id"])
            customer_record = self.sql.query_one('SELECT customer_no FROM Customer where id = %s', item["customer_id"])
            item["customer_no"] = customer_record["customer_no"]
            item["case_no"] = case_record["case_no"]


class create(AdministratorHandler):
    def get(self, *args):
        cid = self.request.get('cid') if self.request.get('cid') is not None else u''
        self.sql.cursor.execute('SELECT case_name, customer_id FROM CaseInfo where id = %s', cid)
        case_record = self.sql.cursor.fetchone()
        self.case_name = case_record[0]
        self.sql.cursor.execute('SELECT customer_name FROM Customer where id = %s', case_record[1])
        customer_record = self.sql.cursor.fetchone()
        self.customer_name = customer_record[0]

    def post(self, *args):
        cid = self.request.get('cid') if self.request.get('cid') is not None else u''
        self.sql.cursor.execute('SELECT customer_id FROM CaseInfo where id = %s', cid)
        case_record = self.sql.cursor.fetchone()
        customer_id = case_record[0]

        equipment_no = self.request.get('equipment_no') if self.request.get('equipment_no') is not None else u''
        equipment_name = self.request.get('equipment_name') if self.request.get('equipment_name') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''
        equipment_id = str(customer_id) + "-" + cid + "-" + equipment_no

        self.sql.cursor.execute('SELECT * FROM Equipment where equipment_id = %s', equipment_id)
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'設備資料新增失敗', "content": u"此客戶已有相同編號的設備，請換一個。"})
            return

        self.sql.cursor.execute('INSERT INTO Equipment (equipment_id, equipment_name, equipment_no, image, is_enable, case_id, customer_id) VALUES (%s, %s, %s, %s, %s, %s, %s'
                                ')', (equipment_id, equipment_name, equipment_no, image, '1', cid, customer_id))

        self.json({"info": u'設備資料已新增', "content": u"您已經成功的新增了一筆設備資料。"})


class edit(AdministratorHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, equipment_id, equipment_name, equipment_no, image, is_enable, case_id, customer_id FROM Equipment where id = %s', id)
            record = self.sql.cursor.fetchone()

            self.sql.cursor.execute('SELECT case_name FROM CaseInfo where id = %s', record[6])
            case_record = self.sql.cursor.fetchone()
            self.sql.cursor.execute('SELECT customer_name FROM Customer where id = %s', record[7])
            customer_record = self.sql.cursor.fetchone()

            self.record = {
                "id": record[0],
                "equipment_id": record[1],
                "equipment_name": record[2],
                "equipment_no": record[3],
                "image": record[4],
                "is_enable": (record[5] == 1),
                "case_name": case_record[0],
                "customer_name": customer_record[0]
            }

    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        equipment_no = self.request.get('equipment_no') if self.request.get('equipment_no') is not None else u''
        equipment_name = self.request.get('equipment_name') if self.request.get('equipment_name') is not None else u''
        image = self.request.get('image') if self.request.get('image') is not None else u''

        self.sql.cursor.execute('SELECT customer_id, case_id FROM Equipment where id = %s', id)
        old_record = self.sql.cursor.fetchone()

        equipment_id = str(old_record[0]) + "-" + str(old_record[1]) + "-" + equipment_no

        self.sql.cursor.execute('SELECT * FROM Equipment where equipment_id = %s And id != %s', (equipment_id, id))
        if self.sql.cursor.rowcount > 0:
            self.json({"info": u'設備資料更新失敗', "content": u"此客戶已有相同編號的設備，請換一個。"})
            return

        self.sql.cursor.execute('SELECT id FROM Equipment where id = %s', id)
        if self.sql.cursor.rowcount == 0:
            self.json({"info": u'設備資料更新失敗', "content": u"此記錄已不存在，可能已被刪除。"})
            return
        else:
            self.sql.cursor.execute('UPDATE Equipment SET equipment_name = %s, equipment_no = %s, image = %s, equipment_id = %s where id = %s',
                                    (equipment_name, equipment_no, image, equipment_id, id))
            self.json({"info": u'設備資料已更新', "content": u"您已經成功的變更了此筆設備資料。"})