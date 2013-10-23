#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26
from libs.yooframework.handler import BaseHandler
from webapp2_extras import sessions


class HomeHandler(BaseHandler):
    def app_init(self):
        self.size = self.params.get_integer("size", 10)
        self.page = self.params.get_integer("page", 1)
        self.page_now = self.page
        self.banner_list = self.sql.query_all('SELECT * FROM Banner WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', (0, 5))
        self.marquee_list = self.sql.query_all('SELECT * FROM Marquee WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', (0, 25))

        self.current_user = None
        if "member_id" in self.session:
            if self.session["member_id"] != "0":
                self.current_user = self.sql.query_one("select * from Member Where id = %s", self.session["member_id"])
        self.cart_count = "%04d" % 0
        self.cart_title = u"尚未選購產品"
        if "order_id" in self.session:
            order = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', self.session["order_id"])
            if order is not None:
                self.cart_count = "%04d" % order["items_count"]
                self.cart_title = u"購買 %d 種產品，共計 %d 個，金額為 %6.2f 元" % (order["items_count"], order["items_total"], order["total_amount"])
