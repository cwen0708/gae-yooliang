#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26
from libs.yooframework.handler import BaseHandler
from webapp2_extras import sessions
from datetime import datetime
from datetime import timedelta


class HomeHandler(BaseHandler):
    def init(self):
        self.today = datetime.today() + timedelta(hours=+8)
        self.yesterday = self.today + timedelta(hours=-24)

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)
        self.size = self.params.get_integer("size", 10)
        self.page = self.params.get_integer("page", 1)
        self.page_now = self.page
        self.init()
        super(BaseHandler, self).dispatch()
        if self.environ.template_already_render is False:
            self.render(None)
        self.session_store.save_sessions(self.response)

    def get_statistics_data_by_equipment_id(self, equipment_id, date):
        self.sql.cursor.execute('SELECT id, kwh FROM StatisticsData where equipment_id = %s and date = %s', (equipment_id, date))
        statistics_record = self.sql.cursor.fetchone()
        if self.sql.cursor.rowcount > 0:
            return statistics_record[1]
        else:
            return 0.0

    def get_statistics_data(self, customer_id, case_id, date):
        self.sql.cursor.execute('SELECT id, kwh FROM StatisticsData where customer_id = %s and case_id = %s and date = %s', (customer_id, case_id, date))
        statistics_record = self.sql.cursor.fetchone()
        if self.sql.cursor.rowcount > 0:
            return statistics_record[1]
        else:
            return 0.0

    def insert_statistics_data(self, customer_id, case_id, kwh, date, last_date):
        self.sql.cursor.execute('SELECT id FROM StatisticsData where customer_id = %s and case_id = %s and date = %s', (customer_id, case_id, date))
        statistics_record = self.sql.cursor.fetchone()
        if self.sql.cursor.rowcount > 0:
            self.sql.cursor.execute('UPDATE StatisticsData SET kwh = %s where id = %s',(kwh, statistics_record[0]))
        else:
            self.sql.cursor.execute('SELECT id, kwh FROM StatisticsData where customer_id = %s and case_id = %s and date = %s', (customer_id, case_id, last_date))
            last_record = self.sql.cursor.fetchone()
            if self.sql.cursor.rowcount > 0:
                last_kwh = float(last_record[1])
            else:
                last_kwh = 0.0
            self.sql.cursor.execute('INSERT INTO StatisticsData (customer_id, case_id, kwh, last_kwh, date) VALUES (%s, %s,%s, %s, %s)', (customer_id, case_id, kwh, last_kwh, date))

