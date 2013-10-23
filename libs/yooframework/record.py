#!/usr/bin/env python
# -*- coding: utf-8 -*-
from application.backend.handler import AdministratorHandler
from libs.yooframework.database import *
import datetime
import logging


class sort(AdministratorHandler):
    def post(self, *args):
        table = self.request.get('t') if self.request.get('t') is not None else ''
        node_list = self.request.get_all('node[]') if self.request.get_all('node[]') is not None else u''
        record_list = self.request.get_all('rec[]') if self.request.get_all('rec[]') is not None else u''
        sort_list = sorted(node_list, reverse=True)
        j = 0
        for item in record_list:
            d = datetime.datetime.fromtimestamp(float(sort_list[j]))
            logging.info('UPDATE ' + table + ' SET sort = %s where id = %s', (d, item))
            self.sql.update(table, {
                "sort": d,
            }, {
                "id": item
            })
            j += 1
        self.json({"action":"sort"})


class delete(AdministratorHandler):
    def post(self, *args):
        table = self.request.get('t') if self.request.get('t') is not None else ''
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if table == '':
            self.json({"action": "error", "record": id})
        if id != '':
            try:
                self.sql.update(table, {
                    "is_delete": "1",
                }, {
                    "id": id
                })
                self.json({"action": "delete", "record": id})
            except:
                self.json({"action": "error", "record": id})


class recovery(AdministratorHandler):
    def post(self, *args):
        table = self.request.get('t') if self.request.get('t') is not None else ''
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if table == '':
            self.json({"action": "error", "record": id})
        if id != '':
            try:
                self.sql.update(table, {
                    "is_delete": "0",
                }, {
                    "id": id
                })
                self.json({"action": "recovery", "record": id})
            except:
                self.json({"action": "error", "record": id})


class real_delete(AdministratorHandler):
    def post(self, *args):
        table = self.request.get('t') if self.request.get('t') is not None else ''
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if table == '':
            self.json({"action": "error", "record": id})
        if id != '':
            try:
                self.sql.delete(table, {
                    "id": id
                })
                self.json({"action": "real_delete", "record": id})
            except:
                self.json({"action": "error", "record": id})

class enable(AdministratorHandler):
    def post(self, *args):
        table = self.request.get('t') if self.request.get('t') is not None else ''
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if table == '':
            self.json({"action": "error", "record": id})
        if id != '':
            try:
                self.sql.update(table, {
                    "is_enable": "1",
                }, {
                    "id": id
                })
                self.json({"action": "enable", "record": id})
            except:
                self.json({"action": "error", "record": id})


class disable(AdministratorHandler):
    def post(self, *args):
        table = self.request.get('t') if self.request.get('t') is not None else ''
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if table == '':
            self.json({"action": "error", "record": id})
        if id != '':
            try:
                self.sql.update(table, {
                    "is_enable": "0",
                }, {
                    "id": id
                })
                self.json({"action": "disable", "record": id})
            except:
                self.json({"action": "error", "record": id})