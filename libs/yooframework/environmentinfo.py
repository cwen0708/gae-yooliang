#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/8/21
import os
from application import RELATIONSHIP


class EnvironmentInfo():
    def __init__(self):
        try:
            self.app_version = str(__file__).split("/")[6]
        except IndexError:
            import random
            self.app_version = random.random()

        self.host = os.environ["SERVER_NAME"]
        self.port = os.environ["SERVER_PORT"]
        for item in RELATIONSHIP:
            if item["host"] == self.host:
                self.app_name = item["app"]

        try:
            theme_name = u""
            exec "from application.%s import THEME_NAME as theme_name" % self.app_name
            self.theme_name = theme_name
        except:
            self.theme_name = u""

        try:
            customer_name = u""
            exec "from application.%s import CUSTOMER_NAME as customer_name" % self.app_name
            self.customer_name = customer_name
        except:
            self.customer_name = u""

        try:
            cloud_storage_bucket = u""
            exec "from application.%s import CLOUD_STORAGE_BUCKET as cloud_storage_bucket" % self.app_name
            self.cloud_storage_bucket_name = cloud_storage_bucket
        except:
            self.customer_name = u""

        if self.port == "80":
            self.base_url = "http://" + self.host
        else:
            self.base_url = "http://" + self.host + ":" + self.port

        self.template_root = os.path.dirname(__file__.split('libs')[0])
        self.template_root = os.path.join(self.template_root, 'template')
        self.template_already_render = False

        cloud_sql_instance_name = u""
        if self.host != "localhost":
            exec "from application.%s import CLOUD_SQL_INSTANCE_NAME as cloud_sql_instance_name" % self.app_name
        self.cloud_sql_instance_name = cloud_sql_instance_name

        cloud_sql_database_name = u""
        exec "from application.%s import CLOUD_SQL_DATABASE as cloud_sql_database_name" % self.app_name
        self.cloud_sql_database_name = cloud_sql_database_name


THEME_NAME = u"0001"
DATABASE_NAMESPACE = u"d0001_epinlady"
CLOUD_SQL_DATABASE = u"d0001_epinlady"
CLOUD_SQL_INSTANCE_NAME = u"yooliang-technology:database"
CLOUD_STORAGE_BUCKET = u"/template.yooliang.com/"