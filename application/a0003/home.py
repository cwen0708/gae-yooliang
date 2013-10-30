#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from handler import HomeHandler
from libs.dateutil import parser
from libs.yooframework.api import random_string, validate_email
from google.appengine.api import mail


class Index(HomeHandler):
    def get(self, *args):
        import random
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.list = self.sql.query_all('SELECT * FROM PastCase WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        random.shuffle(self.list)
        try:
            self.link_01 = "case_view.html?id=" + str(self.list[0]["id"])
            self.image_01 = self.list[0]["image"]
        except IndexError:
            self.link_01 = "case_list.html"
            self.image_01 = "images/testimg01.jpg"
        try:
            self.link_02 = "case_view.html?id=" + str(self.list[1]["id"])
            self.image_02 = self.list[1]["image"]
        except IndexError:
            self.link_02 = "case_list.html"
            self.image_02 = "images/testimg02.jpg"
        try:
            self.link_03 = "case_view.html?id=" + str(self.list[2]["id"])
            self.image_03 = self.list[2]["image"]
        except IndexError:
            self.link_03 = "case_list.html"
            self.image_03 = "images/testimg01.jpg"
        try:
            self.link_04 = "case_view.html?id=" + str(self.list[3]["id"])
            self.image_04 = self.list[3]["image"]
        except IndexError:
            self.link_04 = "case_list.html"
            self.image_04 = "images/testimg02.jpg"


class About(HomeHandler):
    def get(self, *args):
        if self.is_ajax:
            self.render("/about_ajax.html")


class Contact(HomeHandler):
    def get(self, *args):
        if self.is_ajax:
            self.render("/contact_ajax.html")


class CaseList(HomeHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 2)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM PastCase WHERE is_enable = 1 AND is_delete = 0', (), size)
        self.list = self.sql.query_all('SELECT * FROM PastCase WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        for item in self.list:
            if item["images"] is not None and item["images"] is not u"" and item["images"] is not "":
                item["image_list"] = item["images"].split(",")

        self.prev_page = page - 1 if page > 1 else 1
        self.next_page = page + 1 if page < self.page_all else self.page_all
        if self.is_ajax:
            self.render("/case_list_ajax.html")

class CaseView(HomeHandler):
    def get(self, *args):
        self.record = self.sql.query_by_id("PastCase", self.params.get_integer("id"))
        if self.record["images"] is not None and self.record["images"] is not u"" and self.record["images"] is not "":
            self.record["image_list"] = self.record["images"].split(",")

        if self.is_ajax:
            self.render("/case_view_ajax.html")


class HotList(HomeHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 2)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM HotCase WHERE is_enable = 1 AND is_delete = 0', (), size)
        self.list = self.sql.query_all('SELECT * FROM HotCase WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        for item in self.list:
            if item["images"] is not None and item["images"] is not u"" and item["images"] is not "":
                item["image_list"] = item["images"].split(",")

        self.prev_page = page - 1 if page > 1 else 1
        self.next_page = page + 1 if page < self.page_all else self.page_all
        if self.is_ajax:
            self.render("/hot_list_ajax.html")

class HotView(HomeHandler):
    def get(self, *args):
        self.record = self.sql.query_by_id("HotCase", self.params.get_integer("id"))
        if self.record["images"] is not None and self.record["images"] is not u"" and self.record["images"] is not "":
            self.record["image_list"] = self.record["images"].split(",")

        if self.is_ajax:
            self.render("/hot_view_ajax.html")