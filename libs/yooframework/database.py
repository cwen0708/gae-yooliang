#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.api import rdbms
from environmentinfo import EnvironmentInfo


class CloudSQL():
    def __init__(self, instance, database, user, password):
        self.__sql_connect__ = rdbms.connect(instance=instance, database=database, user=user, password=password)
        self.__sql_cursor__ = self.__sql_connect__.cursor()
        self.cursor = self.__sql_cursor__

    def update(self, table_name, new_params=None, where_params=None):
        if not new_params:new_params = {}
        str_new_key = []
        str_new_val = []
        str_where = []
        for key, value in new_params.items():
            str_new_key.append(key + ' = %s')
            str_new_val.append(value)
        for key, value in where_params.items():
            str_where.append(key + ' = %s')
            str_new_val.append(value)
        str_sql = 'UPDATE %s SET %s WHERE %s' % (table_name, (",".join(str(x) for x in str_new_key)), (",".join(str(x) for x in str_where)))
        self.__sql_cursor__.execute(str_sql, str_new_val)

    def insert(self, table_name, params=None):
        str_key = []
        str_temp_val = []
        str_val = []
        for key, value in params.items():
            str_key.append(key)
            str_temp_val.append('%s')
            str_val.append(value)
        str_sql = 'INSERT INTO %s ( %s ) VALUES ( %s )' % (table_name, (",".join(str(x) for x in str_key)), (",".join(str(x) for x in str_temp_val)))
        self.__sql_cursor__.execute(str_sql, str_val)

    def query_by_id(self, table_name, id):
        return self.query_one('select * from ' + table_name + ' where id = %s', id)

    def query_all(self, query, params=(), row_id = 0):
        self.__sql_cursor__.execute(query, params)
        temp_result = self.__sql_cursor__.fetchall()
        result = []
        for item in temp_result:
            item_temp = {}
            row_id += 1
            item_temp["row_id"] = row_id
            c = 0
            for column in self.__sql_cursor__.description:
                item_temp[column[0]] = item[c]
                if column[0] == "is_enable":
                    item_temp["is_enable"] = (item_temp["is_enable"] == 1)
                if column[0] == "is_delete":
                    item_temp["is_delete"] = (item_temp["is_delete"] == 1)
                c += 1
            result.append(item_temp)
        return result

    def query_one(self, query, params=()):
        self.__sql_cursor__.execute(query, params)
        temp_result = self.__sql_cursor__.fetchone()
        if temp_result is not None:
            result = {}
            c = 0
            for column in self.__sql_cursor__.description:
                result[column[0]] = temp_result[c]
                if column[0] == "is_enable":
                    result["is_enable"] = (result["is_enable"] == 1)
                if column[0] == "is_delete":
                    result["is_delete"] = (result["is_delete"] == 1)
                c += 1
            return result
        else:
            return None

    def query_many(self, query, size, params=(), row_id=0):
        self.__sql_cursor__.execute(query, params)
        temp_result = self.__sql_cursor__.fetchmany(size)
        result = []
        for item in temp_result:
            item_temp = {}
            row_id += 1
            item_temp["row_id"] = row_id
            c = 0
            for column in self.__sql_cursor__.description:
                item_temp[column[0]] = item[c]
                if column[0] == "is_enable":
                    item_temp["is_enable"] = (item_temp["is_enable"] == 1)
                if column[0] == "is_delete":
                    item_temp["is_delete"] = (item_temp["is_delete"] == 1)
                c += 1
            result.append(item_temp)
        return result

    def delete(self, table_name, where_params=None):
        str_new_val = []
        str_where = []
        for key, value in where_params.items():
            str_where.append(key + ' = %s')
            str_new_val.append(value)
        str_sql = 'DELETE FROM %s WHERE %s' % (table_name, (" and ".join(str(x) for x in str_where)))
        self.__sql_cursor__.execute(str_sql, str_new_val)

    def pager(self, query, params=(), size = 10):
        self.__sql_cursor__.execute(query, params)
        result = self.__sql_cursor__.fetchone()
        all_record = 0
        try:
            all_record = int(result[0])
        finally:
            return int((all_record + size - 1) / size)
