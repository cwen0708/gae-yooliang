#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db

from application.a0002.handler import HomeHandler
from google.appengine.api import mail
from libs.yooframework.api import random_string, validate_email
from libs.dateutil import parser
from datetime import datetime
from datetime import timedelta
import time


class GreenShepherdHandler(HomeHandler):
    def init(self):
        self.today = datetime.today() + timedelta(hours=+8)
        self.yesterday = self.today + timedelta(hours=-24)
        self.first_service = None
        self.service_results = self.sql.query_all('SELECT id, title FROM Service WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort  DESC')
        for item in self.service_results:
            if self.first_service is None:
                self.first_service = item

        self.product_category_list = self.sql.query_all('SELECT * FROM ProductCategory Where parent = 0 AND  is_enable = 1 AND is_delete = 0 ORDER BY sort DESC')
        self.solution_results = self.sql.query_all('SELECT * FROM Solution WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', (0, 999), 0)

        if "customer_id" not in self.session:
            self.session["customer_id"] = u""
        if self.session["customer_id"] is u"":
            self.user_login = False
        else:
            self.user_login = True

        minute_t = self.today + timedelta(minutes=-5)
        minute = (int(minute_t.strftime("%M")) // 5) * 5
        last_minute_t = self.today + timedelta(minutes=-10)
        last_minute = (int(last_minute_t.strftime("%M")) // 5) * 5

        r1 = self.sql.query_one('SELECT sum(kwh) as total_kwh_1 FROM StatisticsData WHERE date = %s ORDER BY sort DESC LIMIT %s, %s', (minute_t.strftime("minute-%Y-%m-%d %H:") + str(minute), 0, 1))
        r2 = self.sql.query_one('SELECT sum(kwh) as total_kwh_2 FROM StatisticsData WHERE date = %s ORDER BY sort DESC LIMIT %s, %s', (last_minute_t.strftime("minute-%Y-%m-%d %H:") + str(last_minute), 0, 1))
        _total_kwh_1 = r1["total_kwh_1"]
        _total_kwh_2 = r2["total_kwh_2"]
        #_total_kwh_1 = 14980.001
        #_total_kwh_2 = 4980.001
        if _total_kwh_1 is not None:
            self.last_5_minute_kwh = _total_kwh_1 - _total_kwh_2
            self.last_5_minute_total_kwh = _total_kwh_1
            if self.last_5_minute_kwh < 0:
                self.last_5_minute_kwh *= -1

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
                #self.cart_title = u"購買 %d 種產品，共計 %d 個，金額為 %6.2f 元" % (order["items_count"], order["items_total"], order["total_amount"])


    def gen_product_category_list(self):
        category = self.params.get_integer("category", 0)
        parent = self.params.get_integer("parent", 0)
        self.in_parent_category = None
        for item in self.product_category_list:
            if item["id"] == parent:
                self.in_parent_category = item["category_name"]
            item["is_not_root"] = False
            item["is_selected"] = (item["id"] == parent)
            item["link"] = "product.html?parent=" + str(item["id"])
            sub_list = self.sql.query_all('SELECT * FROM ProductCategory Where parent = %s and is_enable = 1 and is_delete = 0 ORDER BY sort DESC', item["id"])

            for item_sub in sub_list:
                if item_sub["id"] == category:
                    self.in_category = item_sub["category_name"]
                item_sub["is_not_root"] = True,
                item_sub["is_selected"] = (item_sub["id"] == category)
                item_sub["link"] = "product.html?parent=" + str(item["id"]) + "&category=" + str(item_sub["id"])
            item["sub_list"] = sub_list

class index(GreenShepherdHandler):
    def get(self, *args):
        self.marquee_list = self.sql.query_all('SELECT content FROM Marquee WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort  DESC LIMIT %s, %s', (0, 25))
        self.banner_list = self.sql.query_all('SELECT * FROM Banner WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort  DESC LIMIT %s, %s', (0, 25))


class learn(GreenShepherdHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.faq_category_list = self.sql.query_all('SELECT id, category_name, is_enable, is_delete, sort FROM FaqCategory Where parent = 0 and is_enable = 1 and is_delete = 0 ORDER BY sort DESC')
        str_category = self.request.get("category") if self.request.get("category") is not None and self.request.get("category") is not "" else u""
        if str_category is u"":
            category = 0
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq Where is_enable = 1 and is_delete = 0', (), size)
            self.faq_list = self.sql.query_all('SELECT * FROM Faq Where is_enable = 1 and is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        else:
            category = int(str_category)
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq Where is_enable = 1 and is_delete = 0 and category = %s', category, size)
            self.faq_list = self.sql.query_all('SELECT * FROM Faq Where is_enable = 1 and is_delete = 0 and category = %s ORDER BY sort DESC LIMIT %s, %s', (category, (page - 1) * size, size))
        for item in self.faq_category_list:
            item["link"] = "/learn.html?category=" + str(item["id"])
            item["is_selected"] = (item["id"] == category)
            if item["id"] == category:
                self.category_name = u" > " + item["category_name"]


class learn_view(GreenShepherdHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, title, content, category, create_date, is_enable FROM Faq where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "category": record[3],
                "create_date": record[4],
                "is_enable": (record[5] == 1)
            }


class about(GreenShepherdHandler):
    def get(self, *args):
        page = 1
        size = 100
        self.sql.cursor.execute('SELECT id, title, content, image FROM Aboutus WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort  DESC LIMIT %s, %s', ((page - 1) * size, size))
        self.rowcount = self.sql.cursor.rowcount
        results = self.sql.cursor.fetchall()
        row_id = (page - 1) * size
        self.results = []
        for item in results:
            row_id += 1
            if row_id % 2 == 0:
                image_pos_left = False
            else:
                image_pos_left = True

            item_temp = {
                "row_id": row_id,
                "id": item[0],
                "title": item[1],
                "content": item[2],
                "image": item[3],
                "image_pos_left": image_pos_left
            }
            self.results.append(item_temp)


class bcastr(HomeHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 100)
        page = self.params.get_integer("page", 1)

        self.sql.cursor.execute('SELECT count(1) FROM Banner WHERE is_enable = 1')
        results = self.sql.cursor.fetchone()
        self.page_now = page
        self.page_all = self.get_page_count(results[0], size)

        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no like "%report_email_%"')
        self.rowcount = self.sql.cursor.rowcount
        results = self.sql.cursor.fetchall()
        row_id = (page - 1) * size
        self.results = []
        for item in results:
            row_id += 1
            item_temp = {
                "row_id": row_id,
                "value": item[0],
            }
            self.results.append(item_temp)
        self.render("/bcastr.html")


class login(GreenShepherdHandler):
    def get(self, *args):
        pass


class service(GreenShepherdHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, title, content, image,  is_enable, is_delete FROM Service where id = %s', id)
            record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "image": record[3],
                "is_enable": (record[4] == 1),
                "is_delete": (record[5] == 1)
            }
            if (record[4] == 0) or (record[5] == 1):
                Here = self
                some = None
                Here.are = some.problems


class solution_view(GreenShepherdHandler):
    def get(self, *args):
        id = self.params.get_integer("id", 0)
        self.sql.cursor.execute('SELECT id, title, content, image, full_content FROM Solution WHERE id = %s', id)
        record = self.sql.cursor.fetchone()
        self.item = {
                "id": record[0],
                "title": record[1],
                "content": record[2],
                "image": record[3],
                "full_content": record[4],
        }


class solution(GreenShepherdHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_all = self.sql.pager('SELECT count(1) FROM Solution WHERE is_enable = 1 AND is_delete = 0 ', (), size)
        self.results = self.sql.query_all('SELECT * FROM Solution WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', (0, 999), 0)


class user_login(HomeHandler):
    def post(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        pw = self.request.get('pw') if self.request.get('pw') is not None else ''
        self.sql.cursor.execute('SELECT id, customer_name FROM Customer WHERE account = %s and password = %s', (id, pw))
        record = self.sql.cursor.fetchone()
        if self.sql.cursor.rowcount > 0:
            self.session["customer_id"] = record[0]
            self.session["customer_name"] = record[1]
            self.json({"info": u"done"})
        else:
            self.json({"info": u"帳號或密碼有誤"})


class watermark(HomeHandler):
    def get(self, *args):
        from google.appengine.api import images
        from google.appengine.api import urlfetch
        image = images.Image(urlfetch.Fetch(self.request.get("image")).content)
        watermark = urlfetch.Fetch(self.request.get('watermark') if self.request.get('watermark') is not None else 'http://upload.wikimedia.org/wikipedia/commons/5/58/Red_copyright.png').content
        new_image = images.composite([(image, 0, 0, 1.0, images.TOP_LEFT),(watermark, 0, 0, 0.5, images.BOTTOM_RIGHT)],image.width,image.height,0, images.PNG)
        self.response.headers['Content-Type'] = "image/png"
        self.response.out.write(new_image)
        self.environ.template_already_render = True


class user_logout(HomeHandler):
    def get(self, *args):
        self.session["customer_id"] = u""
        self.session["customer_name"] = u""
        self.redirect("/index.html")


class error(HomeHandler):
    def get(self, *args):
        Here = self
        some = None
        Here.are = some.problems


class monitor_detail_year(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/jump_to_index.html")
            return

        case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''
        year = self.request.get('year') if self.request.get('year') is not None else u''
        month = self.request.get('month') if self.request.get('month') is not None else u''
        day = self.request.get('day') if self.request.get('day') is not None else u''
        self.sql.cursor.execute('SELECT id, case_name, image, kw, max_kw, start_kwh, price, last_update FROM CaseInfo WHERE id = %s ORDER BY sort', case_id)
        item = self.sql.cursor.fetchone()
        self.case = {
            "id": item[0],
            "case_name": item[1],
            "image": item[2],
            "kw": item[3],
            "max_kw": item[4],
            "start_kw": item[5],
            "last_update": item[7]
        }
        self.results = []
        for i in xrange(0, 11):
            the_month_0 = datetime.strptime(year + "/" + str(i+1) + "/01 00:00:00", '%Y/%m/%d %H:%M:%S')
            if i == 0:
                the_month_1 = datetime.strptime(str(int(year) - 1) + "/12/01 00:00:00", '%Y/%m/%d %H:%M:%S')
            else:
                the_month_1 = datetime.strptime(year + "/" + str(i) + "/01 00:00:00", '%Y/%m/%d %H:%M:%S')
            the_month_0_kwh = self.get_statistics_data(self.session["customer_id"], case_id, the_month_0.strftime("month-%Y-%m"))
            the_month_1_kwh = self.get_statistics_data(self.session["customer_id"], case_id, the_month_1.strftime("month-%Y-%m"))
            if the_month_1_kwh == 0.0:
                kwh = the_month_0_kwh - float(self.case["start_kw"])
            else:
                kwh = the_month_0_kwh - the_month_1_kwh
            if kwh <= 0:
                kwh = 0
            item_temp = {
                "row_id": i,
                "date": the_month_0.strftime("%m"),
                "kwh": kwh
            }
            self.results.append(item_temp)


class monitor_detail_month(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/jump_to_index.html")
            return
        case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''
        year = self.request.get('year') if self.request.get('year') is not None else u''
        month = self.request.get('month') if self.request.get('month') is not None else u''
        day = self.request.get('day') if self.request.get('day') is not None else u''
        self.sql.cursor.execute('SELECT id, case_name, image, kw, max_kw, start_kwh, price, last_update FROM CaseInfo WHERE id = %s ORDER BY sort', case_id)
        item = self.sql.cursor.fetchone()
        self.case = {
            "id": item[0],
            "case_name": item[1],
            "image": item[2],
            "kw": item[3],
            "max_kw": item[4],
            "start_kw": item[5],
            "last_update": item[7]
        }
        the_day = datetime.strptime(year + "/" + month + "/" + "01 00:00:00", '%Y/%m/%d %H:%M:%S')
        self.results = []
        for i in xrange(0, 31):
            the_day_0 = the_day + timedelta(days=i)
            the_day_1 = the_day + timedelta(days=i-1)
            if int(the_day_0.strftime("%m")) == int(month):
                the_day_0_kwh = self.get_statistics_data(self.session["customer_id"], case_id, the_day_0.strftime("day-%Y-%m-%d"))
                the_day_1_kwh = self.get_statistics_data(self.session["customer_id"], case_id, the_day_1.strftime("day-%Y-%m-%d"))
                if the_day_1_kwh == 0.0:
                    kwh = the_day_0_kwh - float(self.case["start_kw"])
                else:
                    kwh = the_day_0_kwh - the_day_1_kwh
                if kwh <= 0:
                    kwh = 0
                item_temp = {
                    "row_id": i,
                    "date": the_day_0.strftime("%d"),
                    "kwh": kwh
                }
                self.results.append(item_temp)


class monitor_detail_week(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/jump_to_index.html")
            return

        case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''
        year = self.request.get('year') if self.request.get('year') is not None else u''
        month = self.request.get('month') if self.request.get('month') is not None else u''
        day = self.request.get('day') if self.request.get('day') is not None else u''
        self.sql.cursor.execute('SELECT id, case_name, image, kw, max_kw, start_kwh, price, last_update FROM CaseInfo WHERE id = %s ORDER BY sort', case_id)
        item = self.sql.cursor.fetchone()
        self.case = {
            "id": item[0],
            "case_name": item[1],
            "image": item[2],
            "kw": item[3],
            "max_kw": item[4],
            "start_kw": item[5],
            "last_update": item[7]
        }
        the_day = datetime.strptime(year + "/" + month + "/" + day + " 00:00:00", '%Y/%m/%d %H:%M:%S')
        self.results = []
        for i in xrange(0, 7):
            the_day_0 = the_day + timedelta(days=-i)
            the_day_1 = the_day + timedelta(days=-i-1)
            the_day_0_kwh = self.get_statistics_data(self.session["customer_id"], case_id, the_day_0.strftime("day-%Y-%m-%d"))
            the_day_1_kwh = self.get_statistics_data(self.session["customer_id"], case_id, the_day_1.strftime("day-%Y-%m-%d"))
            if the_day_1_kwh == 0.0:
                kwh = the_day_0_kwh - float(self.case["start_kw"])
            else:
                kwh = the_day_0_kwh - the_day_1_kwh
            if kwh <= 0:
                kwh = 0
            item_temp = {
                "row_id": 7-i,
                "date": the_day_0.strftime("%m-%d"),
                "kwh": kwh
            }
            self.results.append(item_temp)


class monitor_frame_1(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/jump_to_index.html")
            return
        self.case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''

class monitor_frame_2(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/jump_to_index.html")
            return
        self.case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''


class monitor_realtime(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/jump_to_index.html")
            return
        ex = 0 #28800
        case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''
        total_kwh = self.get_statistics_data(self.session["customer_id"], case_id, self.today.strftime("day-%Y-%m-%d"))
        yesterday_kwh = self.get_statistics_data(self.session["customer_id"], case_id, self.yesterday.strftime("day-%Y-%m-%d"))
        if total_kwh - yesterday_kwh > 0.0:
            today_kwh = total_kwh - yesterday_kwh
        else:
            today_kwh = 0.0
        self.min_time = int(time.mktime(time.strptime(self.today.strftime("%Y-%m-%d 05:00:00"), '%Y-%m-%d %H:%M:%S')))
        self.max_time = int(time.mktime(time.strptime(self.today.strftime("%Y-%m-%d 19:01:00"), '%Y-%m-%d %H:%M:%S')))
        self.sql.cursor.execute('SELECT id, case_name, image, kw, max_kw, price, last_update FROM CaseInfo WHERE id = %s ORDER BY sort', case_id)
        item = self.sql.cursor.fetchone()
        price = float(item[5]) if item[5] is not None else 0
        self.case = {
            "id": item[0],
            "case_name": item[1],
            "image": item[2],
            "kw": item[3],
            "max_kw": item[4],
            "price": price,
            "last_update": item[6],
            "today_kwh": today_kwh,
            "total_kwh": total_kwh,
            "today_price": today_kwh * price
        }
        self.sql.cursor.execute('SELECT id, kwh, kw, UNIX_TIMESTAMP(create_date) FROM RawData WHERE customer_id = %s and case_id = %s and date = %s ORDER BY create_date', (self.session["customer_id"], case_id, self.today.strftime("%Y-%m-%d")))
        self.results = []
        for item in self.sql.cursor.fetchall():
            item_temp = {
                "id": item[0],
                "kwh": item[1],
                "kw": item[2],
                "timestamp": int(item[3]) + ex
            }
            self.results.append(item_temp)


class monitor_info(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/jump_to_index.html")
            return
        case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''
        total_kwh = self.get_statistics_data(self.session["customer_id"], case_id, self.today.strftime("day-%Y-%m-%d"))
        yesterday_kwh = self.get_statistics_data(self.session["customer_id"], case_id, self.yesterday.strftime("day-%Y-%m-%d"))
        if total_kwh - yesterday_kwh > 0.0:
            today_kwh = total_kwh - yesterday_kwh
        else:
            today_kwh = 0.0
        self.sql.cursor.execute('SELECT id, case_name, image, kw, price, last_update FROM CaseInfo WHERE id = %s ORDER BY sort', case_id)
        item = self.sql.cursor.fetchone()
        price = float(item[4]) if item[4] is not None else 0
        self.case = {
            "id": item[0],
            "case_name": item[1],
            "image": item[2],
            "kw": item[3],
            "price": price,
            "last_update": item[5],
            "today_kwh": today_kwh,
            "total_kwh": total_kwh,
            "today_price": today_kwh * price
        }


class Product(GreenShepherdHandler):
    def get(self, *args):
        self.gen_product_category_list()
        category = self.params.get_integer("category", 0)
        parent = self.params.get_integer("parent", 0)
        size = self.params.get_integer("size", 12)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        if category is 0 and parent is 0:
            self.list = self.sql.query_all('SELECT * FROM ProductCategory WHERE parent = 0 AND is_enable = 1 AND is_delete = 0 ORDER BY sort')
            self.render("/product_parent.html")
        else:
            if category is 0:
                self.list = self.sql.query_all('SELECT * FROM ProductCategory WHERE parent = %s AND is_enable = 1 AND is_delete = 0 ORDER BY sort DESC', parent)
                for item in self.list:
                    sub_list = self.sql.query_all('SELECT * FROM Product WHERE category = %s AND is_enable = 1 AND is_delete = 0 ORDER BY  sort DESC LIMIT %s, %s', (item["id"], 0, 3))
                    for sub_item in sub_list:
                        sub_item["link"] = "/product_view.html?parent=" + str(sub_item["parent_category"]) + "&category=" + str(sub_item["category"]) + "&id=" + str(sub_item["id"])
                    item["sub_list"] = sub_list
                    item["link"] = "/product.html?parent=" + str(item["parent"]) + "&category=" + str(item["id"])
                self.render("/product_category.html")
            else:
                self.page_all = self.sql.pager('SELECT count(1) FROM Product WHERE is_enable = 1 AND is_delete = 0 AND category = %s ', category, size)
                self.product_list = self.sql.query_all('SELECT * FROM Product WHERE is_enable = 1 AND is_delete = 0 AND category = %s ORDER BY sort DESC LIMIT %s, %s', (category, (page - 1) * size, size))
                for item in self.product_list:
                    item["link"] = "/product_view.html?parent=" + str(item["parent_category"]) + "&category=" + str(item["category"]) + "&id=" + str(item["id"])


class ProductView(GreenShepherdHandler):
    def get(self, *args):
        self.gen_product_category_list()
        id = self.params.get_integer("id", 1)
        self.record = self.sql.query_by_id("Product", id)
        self.images = self.record["images"].split(",")
        if len(self.images) > 0:
            self.record["image"] = self.images[0]
        else:
            self.record["image"] = "image/no_pic.png"

        self.spec_list = []
        if self.record["price"] is not None:
            spec_list = self.record["price"].split("\n")
            for item in spec_list:
                try:
                    s = item.split("||")
                    self.spec_list.append({
                        "text": s[0],
                        "price": s[1],
                    })
                except:
                    pass
        self.quantity = 50


class project(GreenShepherdHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 50)
        page = self.params.get_integer("page", 1)

        self.sql.cursor.execute('SELECT id, case_name, address, case_no, is_delete, sort, customer_id FROM CaseInfo Where is_enable = 1 and is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        self.rowcount = self.sql.cursor.rowcount
        results = self.sql.cursor.fetchall()
        row_id = (page - 1) * size
        self.results = []
        self.first_project = None
        for item in results:
            row_id += 1
            if self.first_project is None:
                self.first_project = item[0]
            item_temp = {
                "row_id": row_id,
                "id": item[0],
                "title": item[1],
                "address": item[2],
                "case_no": item[3],
                "is_enable": (item[4] == 1),
                "is_delete": (item[5] == 1),
                "sort": item[6]
            }
            self.results.append(item_temp)


class project_detail(GreenShepherdHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.sql.cursor.execute('SELECT id, case_id, case_name, case_no, place, price, address, system_type, complete_date, image, images, is_enable, customer_id FROM CaseInfo where id = %s', id)
            record = self.sql.cursor.fetchone()

            self.sql.cursor.execute('SELECT customer_name FROM Customer where id = %s', record[12])
            customer_record = self.sql.cursor.fetchone()
            self.record = {
                "id": record[0],
                "case_id": record[1],
                "case_name": record[2],
                "case_no": record[3],
                "place": record[4],
                "price": record[5],
                "address": record[6],
                "system_type": record[7],
                "complete_date": record[8],
                "image": record[9],
                "images": record[10],
                "is_enable": (record[11] == 1),
                "customer_id": record[12],
                "customer_name": customer_record[0]
            }
            self.images = []
            if self.record["images"] is not None:
                images = self.record["images"].split(",")
                for item in images:
                    if item != u"" and item != "" and item != " ":
                        self.images.append(item)


class monitor(GreenShepherdHandler):
    def get(self, *args):
        if self.session["customer_id"] is u"":
            self.redirect("/index.html")
            return

        self.customer_name = self.session["customer_name"]
        self.sql.cursor.execute('SELECT id, case_name, image, kw, price, last_update, woeid FROM CaseInfo WHERE customer_id = %s ORDER BY sort', self.session["customer_id"])
        case_list = self.sql.cursor.fetchall()
        self.case_list = []

        case_id = self.request.get('case_id') if self.request.get('case_id') is not None else u''
        if case_id == u'':
            self.case_id = 0
        else:
            self.case_id = int(case_id)

        self.case = None
        for item in case_list:
            self.sql.cursor.execute('SELECT id, equipment_name, last_update, status_code, status_code_time FROM Equipment WHERE case_id = %s ORDER BY sort', item[0])
            equipment_list_temp = self.sql.cursor.fetchall()
            equipment_list = []
            for equipment_item in equipment_list_temp:
                equipment_item_temp = {
                    "id": equipment_item[0],
                    "equipment_name": equipment_item[1],
                    "last_update": equipment_item[2],
                    "status_code": equipment_item[3],
                    "status_code_time": equipment_item[4]
                }
                equipment_list.append(equipment_item_temp)
            price = float(item[4]) if item[4] is not None else 0
            item_temp = {
                "id": item[0],
                "case_name": item[1],
                "image": item[2],
                "kw": item[3],
                "price": price,
                "last_update": item[5],
                "woeid": item[6],
                "equipment_list": equipment_list
            }
            self.case_list.append(item_temp)
            if self.case_id == item[0] or self.case_id == 0:
                self.case_id = item[0]
                self.case = item_temp


class contact_step_1(GreenShepherdHandler):
    def get(self, *args):
        pass


class contact_step_2_1(GreenShepherdHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        self.session["f1"] = u"1"
        f2_1_1 = self.params.get_string("f2_1_1")
        f2_1_2 = self.params.get_string("f2_1_2")

        json_data = {}
        if f2_1_1 is u"":
            json_data["f2_1_1"] = u"請輸入屋頂高度"
        if f2_1_2 is u"":
            json_data["f2_1_2"] = u"請輸入用電情形"
        if len(json_data) > 0:
            return self.json(json_data)
        self.session["f2_1_1"] = f2_1_1
        self.session["f2_1_2"] = f2_1_2
        self.json({"done": u'done', "next": u"contact_step_3.html"})


class contact_step_2_2(GreenShepherdHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        self.session["f1"] = u"2"
        f2_2_1 = self.params.get_string("f2_2_1")
        f2_2_2 = self.params.get_string("f2_2_2")
        json_data = {}
        if f2_2_1 is u"":
            json_data["f2_2_1"] = u"請輸入陽台面積"
        if f2_2_2 is u"":
            json_data["f2_2_2"] = u"請輸入自用 or 售"
        if len(json_data) > 0:
            return self.json(json_data)
        self.session["f2_2_1"] = f2_2_1
        self.session["f2_2_2"] = f2_2_2
        self.json({"done": u'done', "next": u"contact_step_3.html"})

class contact_step_2_3(GreenShepherdHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        self.session["f1"] = u"3"
        f2_3_1 = self.params.get_string("f2_3_1")
        f2_3_2 = self.params.get_string("f2_3_2")
        f2_3_3 = self.params.get_string("f2_3_3")
        f2_3_4 = self.params.get_string("f2_3_4")

        json_data = {}
        if f2_3_1 is u"":
            json_data["f2_3_1"] = u"請輸入可用面積"
        if f2_3_2 is u"":
            json_data["f2_3_2"] = u"請輸入使用電器"
        if f2_3_3 is u"":
            json_data["f2_3_3"] = u"請輸入消耗功率"
        if f2_3_4 is u"":
            json_data["f2_3_4"] = u"請輸入預計使用時間"
        if len(json_data) > 0:
            return self.json(json_data)
        self.session["f2_3_1"] = f2_3_1
        self.session["f2_3_2"] = f2_3_2
        self.session["f2_3_3"] = f2_3_3
        self.session["f2_3_4"] = f2_3_4
        self.json({"done": u'done', "next": u"contact_step_3.html"})

class contact_step_2_4(GreenShepherdHandler):
    def get(self, *args):
        pass
    def post(self, *args):
        self.json({"done": u'done', "next": u"contact_step_3.html"})

class contact_step_2_5(GreenShepherdHandler):
    def get(self, *args):
        pass
    def post(self, *args):
        self.json({"done": u'done', "next": u"contact_step_3.html"})

class contact_step_3(GreenShepherdHandler):
    def get(self, *args):
        pass

    def post(self, *args):
        self.session["f3"] = self.params.get_string("f3")
        self.json({"done": u'done', "next": u"contact_step_4.html"})
    
class contact_step_4(GreenShepherdHandler):
    def get(self, *args):
        pass
    def post(self, *args):
        f4_1 = self.params.get_string("f4_1")
        f4_2 = self.params.get_string("f4_2")
        f4_3 = self.params.get_string("f4_3")
        f4_4 = self.params.get_string("f4_4")
        title = f4_1 + u"留言於 " + self.today.strftime("%Y-%m-%d")

        json_data = {}
        if f4_1 is u"":
            json_data["contact_name"] = u"請輸入聯絡人名稱"
        if f4_2 is u"":
            json_data["contact_tel"] = u"請輸入聯絡電話"
        if f4_3 is u"":
            json_data["contact_address"] = u"請輸入聯絡地址"
        if f4_4 is u"":
            json_data["contact_mail"] = u"請輸入聯絡信箱"
        if len(json_data) > 0:
            return self.json(json_data)

        self.sql.insert("Contact2", {
            "title": title,
            "f1": self.session["f1"],
            "f2_1_1": self.session["f2_1_1"],
            "f2_1_2": self.session["f2_1_2"],
            "f2_2_1": self.session["f2_2_1"],
            "f2_2_2": self.session["f2_2_2"],
            "f2_3_1": self.session["f2_3_1"],
            "f2_3_2": self.session["f2_3_2"],
            "f2_3_3": self.session["f2_3_3"],
            "f2_3_4": self.session["f2_3_4"],
            "f3": self.session["f3"],
            "f4_1": f4_1,
            "f4_2": f4_2,
            "f4_3": f4_3,
            "f4_4": f4_4,
        })
        from google.appengine.api import mail
        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no = %s', "website_mail_sender")
        r = self.sql.cursor.fetchone()
        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no like "%report_email_%"')
        for item in self.sql.cursor.fetchall():
            if item[0] is not "" and item is not None:
                try:
                    mail_body = u"訪客 " + f4_1 + u" 於 " + self.today.strftime("%Y-%m-%d") + u" 留言 <a href='http://www.greenshepherd.com.tw/admin#/admin/contact/list.html'>查看</a>"
                    mail.send_mail(sender=r[0], to=item[0], subject=u"牧陽能控訊息通知", body=mail_body)
                except:
                    pass
        self.json({"done": u'done', "next": u"contact_step_5.html"})
    
class contact_step_5(GreenShepherdHandler):
    def get(self, *args):
        pass


class contact(GreenShepherdHandler):
    def get(self, *args):
        pass

class send_contact_info(HomeHandler):
    def post(self, *args):
        contact_name = self.request.get('contact_name') if self.request.get('contact_name') is not None else u''
        contact_tel = self.request.get('contact_tel') if self.request.get('contact_tel') is not None else u''
        contact_address = self.request.get('contact_address') if self.request.get('contact_address') is not None else u''
        contact_mail = self.request.get('contact_mail') if self.request.get('contact_mail') is not None else u''

        json_data = {}
        if contact_name is u"":
            json_data["contact_name"] = u"請輸入聯絡人名稱"
        if contact_tel is u"":
            json_data["contact_tel"] = u"請輸入聯絡電話"
        if contact_address is u"":
            json_data["contact_address"] = u"請輸入聯絡地址"
        if contact_mail is u"":
            json_data["contact_mail"] = u"請輸入聯絡信箱"
        if len(json_data) > 0:
            return self.json(json_data)

        contact_want_1 = self.request.get('contact_want_1') if self.request.get('contact_want_1') is not None else u''
        contact_want_2 = self.request.get('contact_want_2') if self.request.get('contact_want_2') is not None else u''
        roof_materials = self.request.get('roof_materials') if self.request.get('roof_materials') is not None else u''
        power_number = u''
        for item in self.request.POST.multi._items:
            if item[0] == "power_number":
                if power_number is u"":
                    power_number = item[1]
                else:
                    power_number = power_number + u"," + item[1]
        roof_objects_1 = self.request.get('roof_objects_1') if self.request.get('roof_objects_1') is not None else u''
        roof_objects_2 = self.request.get('roof_objects_2') if self.request.get('roof_objects_2') is not None else u''
        floor_area_1 = self.request.get('floor_area_1') if self.request.get('floor_area_1') is not None else u''
        floor_area_2 = self.request.get('floor_area_2') if self.request.get('floor_area_2') is not None else u''
        floor_area_3 = self.request.get('floor_area_3') if self.request.get('floor_area_3') is not None else u''
        floor_area_4 = self.request.get('floor_area_4') if self.request.get('floor_area_4') is not None else u''
        floor_area_5 = self.request.get('floor_area_5') if self.request.get('floor_area_5') is not None else u''
        floor_area_outside = self.request.get('floor_area_outside') if self.request.get('floor_area_outside') is not None else u''
        floor_area_other = self.request.get('floor_area_other') if self.request.get('floor_area_other') is not None else u''
        title = contact_name + u"留言於 " + self.today.strftime("%Y-%m-%d")

        self.sql.cursor.execute('INSERT INTO Contact ('
                                'title, contact_name, contact_tel, contact_address, contact_want_1, contact_want_2, contact_mail, roof_materials, power_number, roof_objects_1, roof_objects_2, floor_area_1, floor_area_2, floor_area_3, floor_area_4, floor_area_5, floor_area_outside, floor_area_other, is_enable) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                                (title, contact_name, contact_tel, contact_address, contact_want_1, contact_want_2, contact_mail, roof_materials, power_number, roof_objects_1, roof_objects_2, floor_area_1, floor_area_2, floor_area_3, floor_area_4, floor_area_5, floor_area_outside, floor_area_other, '0'))

        from google.appengine.api import mail
        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no = %s', "website_mail_sender")
        r = self.sql.cursor.fetchone()
        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no like "%report_email_%"')
        for item in self.sql.cursor.fetchall():
            if item[0] is not "" and item is not None:
                try:
                    mail_body = u"訪客 " + contact_name + u" 於 " + self.today.strftime("%Y-%m-%d") + u" 留言 <a href='http://www.greenshepherd.com.tw/admin#/admin/contact/list.html'>查看</a>"
                    mail.send_mail(sender=r[0], to=item[0], subject=u"牧陽能控訊息通知", body=mail_body)
                except:
                    pass
        #http://www.greenshepherd.com.tw/admin#/admin/contact/list.html
        self.json({"info": u"done"})

class data_insert(HomeHandler):
    def get(self, *args):
        """ 上傳資料格式: 案場ID, group, string ID, V, I, W,
                KWH_day(INV),KWH_total(INV) -> 32byte/5min /string

            http://localhost:8080/data/insert?customer_no=001&case_no=0001&equipment_no=mid&kwh=30.5
        """
        customer_no = self.request.get('customer_no') if self.request.get('customer_no') is not None else u''
        case_no = self.request.get('case_no') if self.request.get('case_no') is not None else u''
        equipment_no = self.request.get('equipment_no') if self.request.get('equipment_no') is not None else u''
        str_kw = self.request.get('kw') if self.request.get('kw') is not None else u''
        str_kwh = self.request.get('kwh') if self.request.get('kwh') is not None else u''
        if str_kwh == u'':
            self.json({"info": u"Parameter kwh can not be null"})
            return
        try:
            kwh = float(str_kwh)
        except:
            self.json({"info": u"Parameter kwh must be a number"})
            return

        if str_kw == u'':
            self.json({"info": u"Parameter kw can not be null"})
            return
        try:
            kw = float(str_kw)
        except:
            self.json({"info": u"Parameter kw must be a number"})
            return

        self.sql.cursor.execute('SELECT id FROM Customer where customer_no = %s', customer_no)
        customer_record = self.sql.cursor.fetchone()
        if customer_record is None:
            self.json({"info": u"Can not find the customer, make sure that the customer number is correct"})
            return
        else:
            customer_id = customer_record[0]

        self.sql.cursor.execute('SELECT id FROM CaseInfo where customer_id = %s and case_no = %s', (customer_id, case_no))
        case_record = self.sql.cursor.fetchone()
        if case_record is None:
            self.json({"info": u"Can not find the case, make sure the case number is correct"})
            return
        else:
            case_id = case_record[0]

        days = int(self.today.strftime("%d"))
        last_month = self.today + timedelta(days=-days)
        last_year = int(self.today.strftime("%Y")) - 1
        minute = (int(self.today.strftime("%M")) // 5) * 5
        last_minute_t = self.today + timedelta(minutes=-5)
        last_minute = (int(last_minute_t.strftime("%M")) // 5) * 5

        self.insert_statistics_data(customer_id, case_id, kwh, self.today.strftime("year-%Y"), "year-" + str(last_year))
        self.insert_statistics_data(customer_id, case_id, kwh, self.today.strftime("month-%Y-%m"), last_month.strftime("month-%Y-%m"))
        self.insert_statistics_data(customer_id, case_id, kwh, self.today.strftime("day-%Y-%m-%d"), self.yesterday.strftime("day-%Y-%m-%d"))
        self.insert_statistics_data(customer_id, case_id, kwh, self.today.strftime("minute-%Y-%m-%d %H:") + str(minute), last_minute_t.strftime("minute-%Y-%m-%d %H:") + str(last_minute))
        self.sql.cursor.execute('INSERT INTO RawData (customer_id, case_id, kwh, kw, date, create_date) VALUES (%s, %s, %s, %s, %s, %s)', (customer_id, case_id, kwh, kw, self.today.strftime("%Y-%m-%d"), self.today))
        self.sql.cursor.execute('UPDATE CaseInfo SET kw = %s, last_update = %s where id = %s', (kw, self.today, case_id))
        self.json({"info": u"Done"})


class data_equipment_status(HomeHandler):
    def get(self, *args):
        """

        :param args:
        :return:
        """
        customer_no = self.request.get('customer_no') if self.request.get('customer_no') is not None else u''
        case_no = self.request.get('case_no') if self.request.get('case_no') is not None else u''
        equipment_no = self.request.get('equipment_no') if self.request.get('equipment_no') is not None else u''
        status_code = self.request.get('status_code') if self.request.get('status_code') is not None else u''

        self.sql.cursor.execute('SELECT id, customer_name FROM Customer where customer_no = %s', customer_no)
        customer_record = self.sql.cursor.fetchone()
        if customer_record is None:
            self.json({"info": u"Can not find the customer, make sure that the customer number is correct"})
            return
        else:
            customer_id = customer_record[0]

        self.sql.cursor.execute('SELECT id, case_name FROM CaseInfo where customer_id = %s and case_no = %s', (customer_id, case_no))
        case_record = self.sql.cursor.fetchone()
        if case_record is None:
            self.json({"info": u"Can not find the case, make sure the case number is correct"})
            return
        else:
            case_id = case_record[0]

        self.sql.cursor.execute('SELECT id, status_code, status_code_time, equipment_name FROM Equipment where customer_id = %s and case_id = %s and equipment_no = %s', (customer_id, case_id, equipment_no))
        equipment_record = self.sql.cursor.fetchone()
        if equipment_record is None:
            self.json({"info": u"Can not find the device, make sure the device number is correct"})
            return
        else:
            equipment_id = equipment_record[0]

        self.sql.cursor.execute('SELECT id, title, status_code_no, report_time, is_enable FROM StatusCode where status_code_no = %s', status_code)
        status_info_record = self.sql.cursor.fetchone()
        if status_info_record is not None:
            msg = status_info_record[1]
        else:
            msg = status_code

        times = 0
        if equipment_record[1] == msg:
            if equipment_record[2] is None:
                times = 1
            else:
                times = int(equipment_record[2]) + 1
                from google.appengine.api import mail
                if status_info_record is not None:
                    if times == status_info_record[3]:
                        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no = %s', "website_mail_sender")
                        r = self.sql.cursor.fetchone()
                        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no like "%s"', "report_email_")
                        for item in self.sql.cursor.fetchall():
                            if item[0] is not "" and item is not None:
                                try:
                                    mail_body = u"客戶 " + customer_record[1] + u" 的案場 " + case_record[1] + u" 裡的設備 " + equipment_record[3] + u" 發生了 " + msg
                                    mail.send_mail(sender=r[0], to=item[0], subject=u"牧陽能控訊息通知", body=mail_body)
                                except:
                                    pass
        self.sql.cursor.execute('UPDATE Equipment SET last_update = %s, status_code = %s, status_code_time = %s where id = %s', (self.today, msg, times, equipment_id))
        self.json({"info": u"Done"})


class project_flickr(GreenShepherdHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 9999)
        page = self.params.get_integer("page", 1)
        self.page_all = self.sql.pager('SELECT count(1) FROM CaseInfo WHERE is_enable = 1 and is_delete = 0', (), size)
        self.list = self.sql.query_all('SELECT * FROM CaseInfo WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size), (page - 1) * size)


class check_update(HomeHandler):
    def get(self, *args):
        #self.sql.cursor.execute('alter table Equipment add check_time datetime')
        #r = self.sql.cursor.fetchone()

        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no = %s', "check_time")
        r = self.sql.cursor.fetchone()
        seconds = 60 * int(r[0])
        check_time = datetime.today() + timedelta(hours=+8) - timedelta(seconds=+seconds)
        self.sql.cursor.execute('select id, status_code, status_code_time, equipment_name, customer_id, case_id from Equipment Where last_update < %s order by check_time', check_time)
        equipment_record = self.sql.cursor.fetchone()
        if equipment_record is None:
            self.json({"info": u"Everything is ok"})
            return

        self.sql.cursor.execute('SELECT id, title, status_code_no, report_time, is_enable FROM StatusCode where status_code_no = %s', 'out_of_time')
        status_info_record = self.sql.cursor.fetchone()
        if status_info_record is not None:
            msg = status_info_record[1]

        times = 0
        if equipment_record[1] == msg:
            if equipment_record[2] is None:
                times = 1
            else:
                times = int(equipment_record[2]) + 1
            from google.appengine.api import mail
            if status_info_record is not None:
                if times == status_info_record[3]:
                    self.sql.cursor.execute('SELECT id, customer_name FROM Customer where id = %s', equipment_record[4])
                    customer_record = self.sql.cursor.fetchone()
                    if customer_record is None:
                        self.json({"info": u"Can not find the customer, make sure that the customer number is correct"})
                        return
                    else:
                        customer_id = customer_record[0]

                    self.sql.cursor.execute('SELECT id, case_name FROM CaseInfo where id = %s', equipment_record[5])
                    case_record = self.sql.cursor.fetchone()
                    if case_record is None:
                        self.json({"info": u"Can not find the case, make sure the case number is correct"})
                        return
                    else:
                        case_id = case_record[0]

                    self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no = %s', "website_mail_sender")
                    r = self.sql.cursor.fetchone()
                    the_word = u'%%%s%%' % "report_email_"
                    self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no like %s', the_word)
                    for item in self.sql.cursor.fetchall():
                        if item[0] is not "" and item is not None:
                            try:
                                mail_body = u"客戶 " + customer_record[1] + u" 的案場 " + case_record[1] + u" 裡的設備 " + equipment_record[3] + u" 發生了 " + msg
                                mail.send_mail(sender=r[0], to=item[0], subject=u"牧陽能控訊息通知", body=mail_body)
                            except:
                                pass
        self.sql.cursor.execute('UPDATE Equipment SET check_time = %s, status_code = %s, status_code_time = %s where id = %s', (self.today, msg, times, equipment_record[0]))
        self.json({"info": u"Mail notification has been sent"})


class step01(GreenShepherdHandler):
    def get(self, *args):
        self.gen_product_category_list()
        self.page_title = u"購物清單"
        if "order_id" in self.session:
            id = self.session["order_id"]
            if id != '':
                self.record = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', id)
                self.order_item_list = self.sql.query_all('SELECT * FROM OrderItem where order_id = %s', id)
                for item in self.order_item_list:
                    if item["product_spec"] is not None:
                        s = item["product_spec"].split("||")
                        item["spec"] = s[0]
                    else:
                        item["spec"] = u""

                if self.record is not None and len(self.order_item_list) > 0:
                    can_show = True
                else:
                    can_show = False

class step02(GreenShepherdHandler):
    def get(self, *args):
        self.gen_product_category_list()
        self.page_title = u"填寫付款資料"
        self.freighttype_list = self.sql.query_all('SELECT * FROM Freighttype where  is_enable = 1 and is_delete = 0')
        if "order_id" in self.session:
            id = self.session["order_id"]
            if id != '':
                self.record = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', id)


class step02_json(GreenShepherdHandler):
    def post(self, *args):
        if "order_id" not in self.session:
            return self.json({"error": u"訂單已遺失，請重新選擇商品。"})

        pay_type_id = self.params.get_integer("pay_type_id", 0)

        purchaser_name = self.params.get_string("purchaser_name")
        purchaser_email = self.params.get_string("purchaser_email")
        purchaser_mobile = self.params.get_string("purchaser_mobile")
        purchaser_telephone = self.params.get_string("purchaser_telephone")
        purchaser_address_county = self.params.get_string("purchaser_address_county")
        purchaser_address_area = self.params.get_string("purchaser_address_area")
        purchaser_address_detail = self.params.get_string("purchaser_address_detail")

        recipient_name = self.params.get_string("recipient_name")
        recipient_email = self.params.get_string("recipient_email")
        recipient_mobile = self.params.get_string("recipient_mobile")
        recipient_telephone = self.params.get_string("recipient_telephone")
        recipient_address_county = self.params.get_string("recipient_address_county")
        recipient_address_area = self.params.get_string("recipient_address_area")
        recipient_address_detail = self.params.get_string("recipient_address_detail")

        json_data = {}
        if pay_type_id is 0:
            json_data["pay_type_id"] = u"請選擇付款方式"
        if purchaser_name is u"":
            json_data["purchaser_name"] = u"請填寫購買人姓名"
        if purchaser_telephone is u"":
            json_data["purchaser_telephone"] = u"請填寫聯絡電話"
        if purchaser_mobile is u"":
            json_data["purchaser_mobile"] = u"請填寫手機號碼"
        if purchaser_address_county is u"" or purchaser_address_area is u"" or purchaser_address_detail is u"":
            json_data["purchaser_address_detail"] = u"請填寫聯絡地址"

        if recipient_name is u"":
            json_data["recipient_name"] = u"請填寫收件人姓名"
        if recipient_telephone is u"":
            json_data["recipient_telephone"] = u"請填寫聯絡電話"
        if recipient_mobile is u"":
            json_data["recipient_mobile"] = u"請填寫手機號碼"
        if recipient_address_county is u"" or recipient_address_area is u"" or recipient_address_detail is u"":
            json_data["recipient_address_detail"] = u"請填寫聯絡地址"

        if len(json_data) > 0:
            return self.json(json_data)
        if self.is_localhost:
            purchaser_address_county = ""
            purchaser_address_area = ""
            recipient_address_county = ""
            recipient_address_area = ""

        freight_amount = None
        temp = self.sql.query_one('SELECT count(1) as items_count, sum(item_quantity) as items_total, sum(item_sum) as total_amount FROM OrderItem where order_id = %s', self.session["order_id"])
        list = self.sql.query_all("SELECT * FROM Freight WHERE category = %s and is_enable = 1 AND is_delete = 0 ORDER BY sort desc", pay_type_id)
        for i in list:
            if (i["start"]-0.00001) < temp["total_amount"] < (i["end"]+0.00001) and freight_amount is None:
                freight_amount = i["amount"]

        if freight_amount is None:
            freight_amount = 0.0

        self.sql.update("OrderInfo", {
            "pay_type": self.params.get_string("pay_type"),
            "pay_type_id": self.params.get_integer("pay_type_id"),
            "remark": self.params.get_string("remark"),

            "purchaser_name": self.params.get_string("purchaser_name"),
            "purchaser_email": self.params.get_string("purchaser_email"),
            "purchaser_mobile": self.params.get_string("purchaser_mobile"),
            "purchaser_telephone": self.params.get_string("purchaser_telephone"),
            "purchaser_address_county": purchaser_address_county,
            "purchaser_address_area": purchaser_address_area,
            "purchaser_address_zip": self.params.get_string("purchaser_address_zip"),
            "purchaser_address_detail": self.params.get_string("purchaser_address_detail"),

            "recipient_name": self.params.get_string("recipient_name"),
            "recipient_email": self.params.get_string("recipient_email"),
            "recipient_mobile": self.params.get_string("recipient_mobile"),
            "recipient_telephone": self.params.get_string("recipient_telephone"),
            "recipient_address_county": recipient_address_county,
            "recipient_address_area": recipient_address_area,
            "recipient_address_zip": self.params.get_string("recipient_address_zip"),
            "recipient_address_detail": self.params.get_string("recipient_address_detail"),
            "freight": freight_amount
        }, {
            "id": self.session["order_id"]
        })
        return self.json({"done": u"完成"})


class step03(GreenShepherdHandler):
    def get(self, *args):
        self.gen_product_category_list()
        self.page_title = u"確認資料"
        if "order_id" in self.session:
            id = self.session["order_id"]
            if id != '':
                self.record = self.sql.query_one("SELECT * FROM OrderInfo where id = %s", id)
                self.order_item_list = self.sql.query_all('SELECT * FROM OrderItem where order_id = %s', id)
            self.total = int(self.record["total_amount"] + self.record["freight"])


class step03_json(GreenShepherdHandler):
    def get_new_order_no(self):
        today = datetime.today() + timedelta(hours=+8)
        like_string = "%%%s%%" % today.strftime("%Y/%m/%d")
        no = self.sql.query_one("select count(1) as o_count from OrderInfo Where create_date like %s and order_status > 0", like_string)
        return today.strftime("%Y%m%d") + ("-%04d" % (int(no["o_count"])+1))

    def post(self, *args):
        if "order_id" not in self.session:
            return self.json({"error": u"訂單已遺失，請重新選擇商品。"})
        order_id = self.session["order_id"]
        if order_id == '':
            return self.json({"error": u"訂單已遺失，請重新選擇商品。"})
        last_order_no = self.get_new_order_no()
        order_info = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', order_id)

        if self.current_user is not None:
            member_id = self.current_user["id"]
        else:
            d = datetime.today()
            user_account = order_info["purchaser_telephone"]
            check_member = self.sql.query_one('SELECT * FROM Member where user_account = %s', user_account)
            if check_member is not None:
                user_account = user_account + "-" + random_string()
                self.session["auto_member_account_error"] = True

            self.sql.insert('Member', {
                "user_account": user_account,
                "user_password": order_info["purchaser_mobile"],
                "user_name": order_info["purchaser_name"],
                "birthday": d.strftime("%Y-%m-%d"),
                "telephone": order_info["purchaser_telephone"],
                "mobile": order_info["purchaser_mobile"],
                "address_county": order_info["purchaser_address_county"],
                "address_area": order_info["purchaser_address_area"],
                "address_detail": order_info["purchaser_address_detail"],
                "address_zip": order_info["purchaser_address_zip"],
                "email": order_info["purchaser_email"],
                "remark": u'',
                "is_enable": '1',
                "is_custom_account": '0',
            })
            r = self.sql.query_one("SELECT LAST_INSERT_ID() as last_id")
            self.session["auto_member"] = True
            member_id = r["last_id"]
            self.session["member_id"] = member_id

        self.sql.update("OrderInfo", {
            "order_no": last_order_no,
            "title": last_order_no,
            "order_status": 1,
            "pay_status": 0,
            "send_status": 0,
            "member_id": member_id,
        }, {
            "id": self.session["order_id"]
        })
        self.session["last_order_no"] = last_order_no
        self.session["order_id"] = ""
        return self.json({"done": u"完成"})


class step04(GreenShepherdHandler):
    def get(self, *args):
        self.gen_product_category_list()
        self.page_title = u"訂單完成"

        if "auto_member_account_error" in self.session:
            self.auto_member_account_error = self.session["auto_member_account_error"]
        if "auto_member" in self.session:
            self.auto_member = self.session["auto_member"]
        self.last_order_no = self.session["last_order_no"]


        from google.appengine.api import mail
        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no = %s', "website_mail_sender")
        r = self.sql.cursor.fetchone()
        self.sql.cursor.execute('SELECT value FROM WebSetting where setting_no like "%report_email_%"')
        for item in self.sql.cursor.fetchall():
            if item[0] is not "" and item is not None:
                try:
                    url = "http://www.greenshepherd.com.tw/admin#/admin/orderinfo/list.html?order_status=1"
                    mail_body = u"""
    ＊有一筆新的訂單！＊

    訂購人為 %s
    訂購時間為 %s

    更多詳細內容請至 %s 查看。
                """ % (self.current_user["user_name"],(datetime.today() + timedelta(hours=+8)),url)
                    mail.send_mail(sender="gs@greenshepherd.com", to="gs@greenshepherd.com", subject=u"訂單通知", body=mail_body)
                except:
                    pass

class clean_shopping_cart_json(GreenShepherdHandler):
    def post(self, *args):
        if "order_id" in self.session:
            order_id = self.session["order_id"]
            self.json({"done": "完成"})
            self.sql.delete("OrderItem", {
                "order_id": order_id
            })

            temp = self.sql.query_one('SELECT count(1) as items_count, sum(item_quantity) as items_total, sum(item_sum) as total_amount FROM OrderItem where order_id = %s', order_id)
            if temp["items_count"] is None:
                items_count = 0
            else:
                items_count = temp["items_count"]
            if temp["items_total"] is None:
                items_total = 0
            else:
                items_total = temp["items_total"]
            if temp["total_amount"] is None:
                total_amount = 0
            else:
                total_amount = temp["total_amount"]

            if self.current_user is not None:
                member_id = self.current_user["id"]
                self.sql.update("OrderInfo", {
                    "member_id": member_id,
                    "items_count": items_count,
                    "items_total": items_total,
                    "total_amount": total_amount,
                }, {
                    "id": order_id
                })
            else:
                self.sql.update("OrderInfo", {
                    "items_count": items_count,
                    "items_total": items_total,
                    "total_amount": total_amount,
                }, {
                    "id": order_id
                })

class add_shopping_cart_json(GreenShepherdHandler):
    def post(self, *args):
        today = datetime.today() + timedelta(hours=+8)
        product_id = self.params.get_string("product_id")
        quantity = self.params.get_integer("quantity", 0)
        spec = self.params.get_string("spec")

        order = None
        if product_id != '':
            product = self.sql.query_one('SELECT * FROM Product where id = %s', product_id)
        else:
            self.json_message(u"產品不存在")
            return

        spec_can_used = u""
        spec_list = product["price"].split("\n")
        for ss in spec_list:
            if spec.replace("\n", "") == ss.replace("\r", ""):
                spec_can_used = ss

        if spec_can_used is u'':
            self.json_message(u"產品不存在")
            return
        price = float(spec_can_used.split("||")[1].replace("\r", ""))

        if "order_id" in self.session:
            order = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', self.session["order_id"])
            if order is not None:
                create_date = parser.parse(order["create_date"])
                dr = (today - create_date).seconds
                #if dr > 86400:
                #    # 訂單保留時間 86400
                #    self.sql.update("OrderInfo", {
                #        "title": u"this order is out of time",
                #        "order_status": -1,
                #    }, {
                #        "id": order["id"]
                #    })
                #    order = None

        if order is None:
            self.sql.insert("OrderInfo", {
                "order_no": random_string(),
                "title": self.params.get_string(""),
                "items_total": 0,
                "items_count": 0,
                "freight": 0,
                "discount": 0,
                "total_amount": 0,
                "member_id": 0,
                "purchaser_name": self.params.get_string(""),
                "purchaser_email": self.params.get_string(""),
                "purchaser_mobile": self.params.get_string(""),
                "purchaser_telephone": self.params.get_string(""),
                "purchaser_address_county": self.params.get_string(""),
                "purchaser_address_area": self.params.get_string(""),
                "purchaser_address_zip": self.params.get_string(""),
                "purchaser_address_detail": self.params.get_string(""),

                "recipient_name": self.params.get_string(""),
                "recipient_email": self.params.get_string(""),
                "recipient_mobile": self.params.get_string(""),
                "recipient_telephone": self.params.get_string(""),
                "recipient_address_county": self.params.get_string(""),
                "recipient_address_area": self.params.get_string(""),
                "recipient_address_zip": self.params.get_string(""),
                "recipient_address_detail": self.params.get_string(""),

                "pay_type": self.params.get_string(""),
                "pay_type_id": 0,
                "order_status": 0,
                "pay_status": -1,
                "send_status": -1,
                "remark": self.params.get_string(""),
                "create_date": today.strftime("%Y/%m/%d %H:%M:%S")

            })
            r = self.sql.query_one("SELECT LAST_INSERT_ID() as last_id")
            self.session["order_id"] = r["last_id"]
            order = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', self.session["order_id"])
        product_id = product["id"]
        order_id = order["id"]
        member_id = 0
        images = product["images"].split(",")
        if len(images) > 0:
            product_image = images[0]
        else:
            product_image = "image/no_pic.png"

        if quantity < 0:
            self.json({"done": "完成"})
            self.sql.delete("OrderItem", {
                "order_id": order_id,
                "product_id": product_id,
                "product_spec": spec_can_used,
            })
            return
        else:
            order_item = self.sql.query_one('SELECT * FROM OrderItem where order_id = %s and product_id = %s and product_spec = %s', (order_id, product_id, spec_can_used))
            if order_item is None:
                self.sql.insert("OrderItem", {
                    "product_id": product_id,
                    "product_no": product["product_no"],
                    "product_name": product["product_name"],
                    "product_price": price,
                    "product_spec": spec_can_used,
                    "product_image": product_image,
                    "product_url": "/goods_view.html?parent=1&category=5&id=1",
                    "item_quantity": quantity,
                    "item_status": 0,
                    "item_sum": price * quantity,
                    "order_id": order_id,
                })
            else:
                self.sql.update("OrderItem", {
                    "item_quantity": quantity,
                    "item_sum": price * quantity,
                }, {
                    "id": order_item["id"]
                })
        temp = self.sql.query_one('SELECT count(1) as items_count, sum(item_quantity) as items_total, sum(item_sum) as total_amount FROM OrderItem where order_id = %s', order_id)

        if self.current_user is not None:
            member_id = self.current_user["id"]
            self.sql.update("OrderInfo", {
                "member_id": member_id,
                "items_count": temp["items_count"],
                "items_total": temp["items_total"],
                "total_amount": temp["total_amount"],
            }, {
                "id": order_id
            })
        else:
            self.sql.update("OrderInfo", {
                "items_count": temp["items_count"],
                "items_total": temp["items_total"],
                "total_amount": temp["total_amount"],
            }, {
                "id": order_id
            })
        self.json({"done": "完成"})
