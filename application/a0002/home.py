#!/usr/bin/env python
# -*- coding: utf-8 -*-
from google.appengine.ext import db

from application.a0002.handler import HomeHandler

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

        self.before_yesterday = self.yesterday + timedelta(hours=-24)
        r1 = self.sql.query_one('SELECT sum(kwh) as total_kwh_1 FROM StatisticsData WHERE date = %s ORDER BY sort DESC LIMIT %s, %s', (self.yesterday.strftime("day-%Y-%m-%d"), 0, 1))
        r2 = self.sql.query_one('SELECT sum(kwh) as total_kwh_2 FROM StatisticsData WHERE date = %s ORDER BY sort DESC LIMIT %s, %s', (self.before_yesterday.strftime("day-%Y-%m-%d"), 0, 1))
        _total_kwh_1 = r1["total_kwh_1"]
        _total_kwh_2 = r2["total_kwh_2"]
        #_total_kwh_1 = 14980.001
        #_total_kwh_2 = 4980.001
        if _total_kwh_1 is not None:
            self.yesterday_kwh = _total_kwh_1 - _total_kwh_2
            self.yesterday_total_kwh = _total_kwh_1
            if self.yesterday_kwh < 0:
                self.yesterday_kwh *= -1


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


class product(GreenShepherdHandler):
    def get(self, *args):
        category = self.params.get_integer("category", 0)
        parent = self.params.get_integer("parent", 0)
        self.menu_list = []

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

        size = self.params.get_integer("size", 12)
        page = self.params.get_integer("page", 1)

        self.page_now = page
        if category is 0 and parent is 0:
            self.page_all = self.sql.pager('SELECT count(1) FROM Product WHERE is_enable = 1 AND is_delete = 0', (), size)
            self.product_list = self.sql.query_all('SELECT * FROM Product WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        else:
            if category is not 0:
                self.page_all = self.sql.pager('SELECT count(1) FROM Product WHERE is_enable = 1 AND is_delete = 0 AND category = %s', category, size)
                self.product_list = self.sql.query_all('SELECT * FROM Product WHERE is_enable = 1 AND is_delete = 0 AND category = %s  ORDER BY sort DESC LIMIT %s, %s', (category, (page - 1) * size, size))
            else:
                self.page_all = self.sql.pager('SELECT count(1) FROM Product WHERE is_enable = 1 AND is_delete = 0 AND parent_category = %s ', parent, size)
                self.product_list = self.sql.query_all('SELECT * FROM Product WHERE is_enable = 1 AND is_delete = 0 AND parent_category = %s ORDER BY sort DESC LIMIT %s, %s', (parent, (page - 1) * size, size))

        for item in self.product_list:
            item["link"] = "/product_view.html?parent=" + str(item["parent_category"]) + "&category=" + str(item["category"]) + "&id=" + str(item["id"])


class product_view(GreenShepherdHandler):
    def get(self, *args):
        category = self.params.get_integer("category", 0)
        parent = self.params.get_integer("parent", 0)
        self.menu_list = []

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

        id = self.params.get_integer("id", 1)
        self.record = self.sql.query_by_id("Product", id)
        self.images = self.record["images"].split(",")
        if len(self.images) > 0:
            self.record["image"] = self.images[0]
        else:
            self.record["image"] = "image/no_pic.png"


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
class contact_step_2_2(GreenShepherdHandler):
    def get(self, *args):
        pass
class contact_step_2_3(GreenShepherdHandler):
    def get(self, *args):
        pass
class contact_step_2_4(GreenShepherdHandler):
    def get(self, *args):
        pass
class contact_step_2_5(GreenShepherdHandler):
    def get(self, *args):
        pass
class contact_step_3(GreenShepherdHandler):
    def get(self, *args):
        pass
class contact_step_4(GreenShepherdHandler):
    def get(self, *args):
        pass
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

        self.insert_statistics_data(customer_id, case_id, kwh, self.today.strftime("year-%Y") ,"year-" + str(last_year))
        self.insert_statistics_data(customer_id, case_id, kwh, self.today.strftime("month-%Y-%m"), last_month.strftime("month-%Y-%m"))
        self.insert_statistics_data(customer_id, case_id, kwh, self.today.strftime("day-%Y-%m-%d"), self.yesterday.strftime("day-%Y-%m-%d"))
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


