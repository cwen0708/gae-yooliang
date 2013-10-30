#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
from handler import HomeHandler
from libs.dateutil import parser
from libs.yooframework.api import random_string, validate_email
from google.appengine.api import mail


class ProductMenuHandler(HomeHandler):
    def page_init(self):
        tc = self.params.get_integer("tc", 0)
        self.tc = tc
        if tc is 0:
            self.redirect("error.html")
        self.menu_list = []
        pc = self.sql.query_all('SELECT * FROM ProductCategory WHERE is_enable = 1 and is_delete = 0 ORDER BY sort DESC')
        for item in pc:
            if item["parent"] == 0 and item["id"] == tc:
                item["level"] = 0
                item["in_list"] = True
                self.menu_list.append(item)
            else:
                item["in_list"] = False
        # 最大３層
        for i in xrange(0, 3):
            for item in pc:
                if item["in_list"] is not True:
                    for parent_item in self.menu_list:
                        if item["parent"] == parent_item["id"] and parent_item["level"] == i:
                            parent_item["is_parent"] = True
                            item["level"] = (i + 1)
                            item["in_list"] = True
                            item["is_select"] = False
                            index = self.menu_list.index(parent_item) + 1
                            self.menu_list.insert(index, item)


class MemberMenuHandler(HomeHandler):
    def page_init(self):
        self.menu_list = []
        if self.current_user is None:
            self.menu_list.append({"link": u"login.html", "menu_name": u"會員登入", "is_select": self.environ.path.find(u"login.html") > 0})
            self.menu_list.append({"link": u"join.html", "menu_name": u"加入會員", "is_select": self.environ.path.find(u"join.html") > 0})
            self.menu_list.append({"link": u"password.html", "menu_name": u"忘記密碼", "is_select": self.environ.path.find(u"password.html") > 0})
            self.menu_list.append({"link": u"step01.html", "menu_name": u"購物車", "is_select": self.environ.path.find(u"step") > 0})
        else:
            self.menu_list.append({"link": u"info.html", "menu_name": u"會員資料", "is_select": self.environ.path.find(u"info.html") > 0})
            self.menu_list.append({"link": u"password_ch.html", "menu_name": u"修改密碼", "is_select": self.environ.path.find(u"password_ch.html") > 0})
            self.menu_list.append({"link": u"step01.html", "menu_name": u"購物車", "is_select": self.environ.path.find(u"step01.html") > 0})
            self.menu_list.append({"link": u"order.html", "menu_name": u"訂單查詢", "is_select": self.environ.path.find(u"order.html") > 0})
            self.menu_list.append({"link": u"re_question.html", "menu_name": u"問題回覆", "is_select": self.environ.path.find(u"re_question.html") > 0})


class ContactMenuHandler(HomeHandler):
    def page_init(self):
        self.menu_list = []
        self.menu_list.append({"link": u"contact.html", "menu_name": u"地理位置", "is_select": self.environ.path.find(u"contact.html") > 0})
        self.menu_list.append({"link": u"contact_form.html", "menu_name": u"商品諮詢", "is_select": self.environ.path.find(u"contact_form.html") > 0})
        self.menu_list.append({"link": u"sellform.html", "menu_name": u"經銷表單", "is_select": self.environ.path.find(u"sellform.html") > 0})
        self.menu_list.append({"link": u"foreign_form.html", "menu_name": u"韓國市集代購", "is_select": self.environ.path.find(u"foreign_form") > 0})


class Index(HomeHandler):
    def get(self, *args):
        self.banner_style = "iBanner"
        self.banner_height = "450"
        self.banner_list = self.sql.query_all('SELECT * FROM Banner WHERE is_enable = 1 AND is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', (0, 25))

class Contact(HomeHandler):
    def get(self, *args):
        self.record = self.sql.query_one('SELECT * FROM WebPage where setting_no = %s', 'contact')
        if self.record is not None:
            self.page_title = self.record["setting_name"]


class Process(HomeHandler):
    def get(self, *args):
        self.record = self.sql.query_one('SELECT * FROM WebPage where setting_no = %s', 'process')
        if self.record is not None:
            self.page_title = self.record["setting_name"]


class Process02(HomeHandler):
    def get(self, *args):
        self.record = self.sql.query_one('SELECT * FROM WebPage where setting_no = %s', 'process02')
        if self.record is not None:
            self.page_title = self.record["setting_name"]


class Declare(HomeHandler):
    def get(self, *args):
        self.record = self.sql.query_one('SELECT * FROM WebPage where setting_no = %s', 'declare')
        if self.record is not None:
            self.page_title = self.record["setting_name"]

class Faq(HomeHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.category_id = self.params.get_integer("category", 0)
        self.category_list = self.sql.query_all('SELECT * FROM FaqCategory Where parent = 0 and is_enable = 1 and is_delete = 0 ORDER BY sort DESC')

        if self.category_id is 0:
            self.page_title = u"問與答"
            self.nav_title = u"全部"
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq Where is_enable = 1 and is_delete = 0', (), size)
            self.faq_list = self.sql.query_all('SELECT * FROM Faq Where is_enable = 1 and is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        else:
            for item in self.category_list:
                if item["id"] == self.category_id:
                    self.page_title = item["category_name"] + u" - 問與答"
                    self.nav_title = item["category_name"]
            self.page_all = self.sql.pager('SELECT count(1) FROM Faq Where is_enable = 1 and is_delete = 0 and category = %s', self.category_id, size)
            self.faq_list = self.sql.query_all('SELECT * FROM Faq Where is_enable = 1 and is_delete = 0 and category = %s ORDER BY sort DESC LIMIT %s, %s', (self.category_id, (page - 1) * size, size))


class guestbook(ProductMenuHandler):
    def get(self, *args):
        self.page_title = u"留言板"


class guestbook_list(ProductMenuHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 8)
        page = self.params.get_integer("page", 1)
        category = self.params.get_integer("category", 0)
        parent = self.params.get_integer("parent", 0)
        keyword = self.params.get_string("keyword", u"")

        self.page_now = page
        if keyword is u"":
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
        else:
            the_word = u'%%%s%%' % keyword
            if category is 0 and parent is 0:
                self.page_all = self.sql.pager(u'SELECT count(1) FROM Product WHERE is_enable = 1 AND is_delete = 0 AND product_name like %s', the_word, size)
                self.product_list = self.sql.query_all(u"SELECT * FROM Product WHERE is_enable = 1 AND is_delete = 0 AND product_name like %s ORDER BY sort DESC LIMIT %s, %s", (the_word, (page - 1) * size, size))
            else:
                if category is not 0:
                    self.page_all = self.sql.pager(u'SELECT count(1) FROM Product WHERE is_enable = 1 AND is_delete = 0 AND category = %s AND product_name like %s', (the_word, category), size)
                    self.product_list = self.sql.query_all(u'SELECT * FROM Product WHERE is_enable = 1 AND is_delete = 0 AND category = %s AND product_name like %s ORDER BY sort DESC LIMIT %s, %s', (category, the_word, (page - 1) * size, size))
                else:
                    self.page_all = self.sql.pager(u'SELECT count(1) FROM Product WHERE is_enable = 1 AND is_delete = 0 AND parent_category = %s AND product_name like %s', (the_word, parent), size)
                    self.product_list = self.sql.query_all(u'SELECT * FROM Product WHERE is_enable = 1 AND is_delete = 0 AND parent_category = %s AND product_name like %s ORDER BY sort DESC LIMIT %s, %s', (parent, the_word, (page - 1) * size, size))

        for item in self.product_list:
            images = item["images"].split(",")
            if len(images) > 0:
                item["image"] = images[0]
            else:
                item["image"] = "image/no_pic.png"
            item["link"] = "/guestbook_form.html?parent=" + str(item["parent_category"]) + "&category=" + str(item["category"]) + "&id=" + str(item["id"])


class guestbook_form(ProductMenuHandler):
    def get(self, *args):
        self.today = datetime.datetime.today() + datetime.timedelta(hours=+8)
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Product where id = %s', id)
            self.page_title = self.record["product_name"] + u" - 產品詳細資訊"
            self.images = self.record["images"].split(",")
            if len(self.images) > 0:
                self.record["image"] = self.images[0]
            else:
                self.record["image"] = "image/no_pic.png"


class guestbook_json(ProductMenuHandler):
    def post(self, *args):
        product_image = self.params.get_string("product_image")
        product_name = self.params.get_string("product_name")
        product_no = self.params.get_string("product_no")
        product_id = self.params.get_integer("product_id")
        member_id = self.params.get_integer("member_id")
        member_name = self.params.get_string("member_name")
        contact_name = self.params.get_string("contact_name")
        contact_telephone = self.params.get_string("contact_telephone")
        contact_address = self.params.get_string("contact_address")
        buy_date = self.params.get_string("buy_date")
        content = self.params.get_string("content")
        today = datetime.datetime.today() + datetime.timedelta(hours=+8)
        create_date = today.strftime("%Y/%m/%d %H:%M")

        json_data = {}
        if contact_name is u"":
            json_data["contact_name"] = u"請輸入名字"
        if contact_telephone is u"":
            json_data["contact_telephone"] = u"請輸入電話"
        if len(json_data) > 0:
            return self.json(json_data)
        else:
            self.sql.insert("Guestbook", {
                "product_image": product_image,
                "product_name": product_name,
                "product_no": product_no,
                "product_id": product_id,
                "member_id": member_id,
                "member_name": member_name,
                "contact_name": contact_name,
                "contact_telephone": contact_telephone,
                "contact_address": contact_address,
                "buy_date": buy_date,
                "content": content,
                "create_date": create_date,
                "is_enable": 0
            })
            url = "http://www.063318866.com/admin#/admin/guestbook/list.html"
            mail_body = u"""

    ＊有一則新的留言！＊
    留言人   %s
    留言時間 %s
    聯絡電話 %s
    聯絡地址 %s
    購買日期 %s
    =================================================================
    %s
    =================================================================
    更多詳細內容請至 %s 查看。
    """ % (
                contact_name,
                (datetime.datetime.today() + datetime.timedelta(hours=+8)),
                contact_telephone,
                contact_address,
                buy_date,
                content,
                url
            )
            mail.send_mail(sender="service@063318866.com", to="service@063318866.com", subject=u"一品夫人官網留言通知", body=mail_body)

            return self.json({"done": u"感謝您的留言，我們將會儘快回覆您。"})


class goods_list(ProductMenuHandler):
    def get(self, *args):
        tc = self.params.get_integer("tc", 0)
        size = self.params.get_integer("size", 12)
        page = self.params.get_integer("page", 1)
        category = self.params.get_integer("category", 0)
        parent = self.params.get_integer("parent", 0)

        if tc is 0:
            self.redirect("error.html")

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
            images = item["images"].split(",")
            if len(images) > 0:
                item["image"] = images[0]
            else:
                item["image"] = "image/no_pic.png"
            item["link"] = "/goods_view.html?parent=" + str(item["parent_category"]) + "&category=" + str(item["category"]) + "&id=" + str(item["id"])


class goods_view(ProductMenuHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM Product where id = %s', id)
            self.page_title = self.record["product_name"] + u" - 產品詳細資訊"
            self.images = self.record["images"].split(",")
            if len(self.images) > 0:
                self.record["image"] = self.images[0]
            else:
                self.record["image"] = "image/no_pic.png"
        if (self.record["is_enable"] is False or self.record["is_delete"] is True):
            self.redirect("/error.html")
        self.quantity = 50
        if self.quantity > 50:
            self.quantity = 50


class NewsList(ProductMenuHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.category_id = self.params.get_integer("category", 0)
        self.category_list = self.sql.query_all('SELECT * FROM NewsCategory Where parent = 0 and is_enable = 1 and is_delete = 0 ORDER BY sort DESC')

        if self.category_id is 0:
            self.page_title = u"最新消息"
            self.nav_title = u"全部"
            self.page_all = self.sql.pager('SELECT count(1) FROM News Where is_enable = 1 and is_delete = 0', (), size)
            self.faq_list = self.sql.query_all('SELECT * FROM News Where is_enable = 1 and is_delete = 0 ORDER BY sort DESC LIMIT %s, %s', ((page - 1) * size, size))
        else:
            for item in self.category_list:
                if item["id"] == self.category_id:
                    self.page_title = item["category_name"] + u" - 最新消息"
                    self.nav_title = item["category_name"]
            self.page_all = self.sql.pager('SELECT count(1) FROM News Where is_enable = 1 and is_delete = 0 and category = %s', self.category_id, size)
            self.faq_list = self.sql.query_all('SELECT * FROM News Where is_enable = 1 and is_delete = 0 and category = %s ORDER BY sort DESC LIMIT %s, %s', (self.category_id, (page - 1) * size, size))


class NewsView(ProductMenuHandler):
    def get(self, *args):
        id = self.params.get_string("id")
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM News where id = %s', id)
            self.page_title = self.record["title"] + u" - 最新消息"
        self.category_id = self.record["category"]
        self.category_list = self.sql.query_all('SELECT * FROM NewsCategory Where parent = 0 and is_enable = 1 and is_delete = 0 ORDER BY sort DESC')
        if self.category_id is 0:
            self.nav_title = u"全部"
        else:
            for item in self.category_list:
                if item["id"] == self.category_id:
                    self.nav_title = item["category_name"]


class Login(MemberMenuHandler):
    def get(self, *args):
        pass


class login_json(MemberMenuHandler):
    def post(self, *args):
        account = self.params.get_string("account")
        password = self.params.get_string("password")
        if account is u"":
            self.json_message(u"請輸入帳號")
        if password is u"":
            self.json_message(u"請輸入六位數以上的密碼")
        r = self.sql.query_one("select * from Member Where user_account = %s AND user_password = %s", (account, password))
        if r is not None:
            self.session["member_id"] = r["id"]
            self.current_user = r
            self.json_message("done")
            if "order_id" in self.session:
                order_id = self.session["order_id"]
                self.sql.update("OrderInfo", {
                    "member_id": self.current_user["id"],
                }, {
                    "id": order_id
                })
            return
        r = self.sql.query_one("select * from Member Where email = %s AND user_password = %s", (account, password))
        if r is not None:
            self.session["member_id"] = r["id"]
            self.current_user = r
            self.json_message("done")
            if "order_id" in self.session:
                order_id = self.session["order_id"]
                self.sql.update("OrderInfo", {
                    "member_id": self.current_user["id"],
                }, {
                    "id": order_id
                })
            return
        self.json_message(u"帳號密碼有誤")


class logout_json(MemberMenuHandler):
    def post(self, *args):
        self.session["member_id"] = "0"
        self.json_message("done")


class join(MemberMenuHandler):
    def get(self, *args):
        self.page_title = u"加入會員"
        if self.current_user is not None:
            return self.redirect("/info.html")


class join_json(MemberMenuHandler):
    def validateEmail(self, email):
        import re
        if len(email) > 6:
            if re.match('^[a-zA-Z0-9._%-+]+@[a-zA-Z0-9._%-]+.[a-zA-Z]{2,6}$', email) is not None:
                return True
        return False

    def post(self, *args):
        email = self.params.get_string("email")
        password = self.params.get_string("password")
        password2 = self.params.get_string("password2")
        json_data = {}
        if email is u"":
            json_data["email"] = u"請輸入電子信箱"
        if validate_email(email) is False:
            json_data["email"] = u"請電子信箱格式有誤"


        if len(password) < 6:
            json_data["password"] = u"請密碼長度不足"
        if password != password2:
            json_data["password2"] = u"請確認密碼是否一致"
        if password is u"":
            json_data["password"] = u"請輸入密碼"
        if password2 is u"":
            json_data["password2"] = u"請輸入確認密碼"
        r = self.sql.query_one("select * from Member Where email = %s", email)
        if r is not None:
            json_data["email"] = u"此信箱已有人使用"
        if len(json_data) > 0:
            return self.json(json_data)
        else:
            d = datetime.datetime.today()
            self.sql.insert('Member',{
                "user_account": email,
                "user_password": password,
                "user_name": email,
                "birthday": d.strftime("%Y-%m-%d"),
                "telephone": u'',
                "mobile": u'',
                "address_county": u'',
                "address_area": u'',
                "address_detail": u'',
                "address_zip": u'',
                "email": email,
                "remark": u'',
                "is_enable": '1',
                "is_custom_account": '0',
            })
            return self.json({"done": u"感謝您的加入。"})

class password(MemberMenuHandler):
    def get(self, *args):
        self.page_title = u"忘記密碼"

class info(MemberMenuHandler):
    def get(self, *args):
        self.page_title = u"會員資料"
        if self.current_user is None:
            return self.redirect("/join.html")

class info_json(MemberMenuHandler):
    def post(self, *args):
        json_data = {}
        if self.current_user is None:
            json_data["user_name"] = u"您尚未登入，或登入已逾期，請先登入"
            return self.json(json_data)

        if self.current_user["is_custom_account"] == 0:
            user_account = self.params.get_string("user_account")
            if user_account is u"":
                json_data["user_account"] = u"初次設定請填寫會員帳號，設定完成後無法更改"
                return self.json(json_data)
        else:
            user_account = self.current_user["user_account"]

        user_name = self.params.get_string("user_name")
        birthday = self.params.get_string("birthday")
        telephone = self.params.get_string("telephone")
        mobile = self.params.get_string("mobile")
        email = self.params.get_string("email")
        address_county = self.params.get_string("address_county")
        address_area = self.params.get_string("address_area")
        address_zip = self.params.get_string("address_zip")
        address_detail = self.params.get_string("address_detail")

        if self.is_localhost:
            address_county = ""
            address_area = ""
        self.sql.update("Member", {
            "user_account": user_account,
            "user_name": user_name,
            "birthday": birthday,
            "telephone": telephone,
            "mobile": mobile,
            "email": email,
            "address_county": address_county,
            "address_area": address_area,
            "address_zip": address_zip,
            "address_detail": address_detail,
            "is_dealer": 0,
            "is_custom_account": 1,
        }, {
            "id": self.current_user["id"]
        })
        json_data["done"] = u"您的資料已經更新了。"
        return self.json(json_data)


class password_ch(MemberMenuHandler):
    def get(self, *args):
        if self.current_user is None:
            return self.redirect("/")


class password_ch_json(MemberMenuHandler):
    def post(self, *args):
        old_password = self.params.get_string("old_password")
        password = self.params.get_string("password")
        password2 = self.params.get_string("password2")
        json_data = {}
        if self.current_user is None:
            json_data["old_password"] = u"您尚未登入，或登入已逾期，請先登入"
            return self.json(json_data)
        if self.current_user["user_password"] != old_password:
            json_data["old_password"] = u"舊密碼不相符，請重新輸入"
        if len(password) < 6:
            json_data["password"] = u"請密碼長度不足"
        if password != password2:
            json_data["password2"] = u"請確認密碼是否一致"
        if password is u"":
            json_data["password"] = u"請輸入密碼"
        if password2 is u"":
            json_data["password2"] = u"請輸入確認密碼"

        if len(json_data) > 0:
            return self.json(json_data)
        else:
            self.sql.update("Member",{
                "user_password": password
            },{
                "id": self.current_user["id"]
            })
            return self.json({"done": u"您的密碼已經成功變更了。"})


class password_sw(MemberMenuHandler):
    def get(self, *args):
        self.validate_key = self.params.get_string("validate_key")


class password_sw_json(MemberMenuHandler):
    def post(self, *args):
        validate_key = self.params.get_string("validate_key")
        password = self.params.get_string("password")
        password2 = self.params.get_string("password2")
        json_data = {}
        member = self.sql.query_one("select * from Member where validate_key = %s", validate_key)
        if len(password) < 6:
            json_data["password"] = u"請密碼長度不足"
        if password != password2:
            json_data["password2"] = u"請確認密碼是否一致"
        if password is u"":
            json_data["password"] = u"請輸入密碼"
        if password2 is u"":
            json_data["password2"] = u"請輸入確認密碼"

        if member is None:
            json_data["password"] = u"此連結已經失效了，請重新寄發「忘記密碼」郵件"
        if len(json_data) > 0:
            return self.json(json_data)
        else:
            self.sql.update("Member",{
                "user_password": password,
                "validate_key": ""
            },{
                "id": member["id"]
            })
            return self.json({"done": u"您的密碼已經成功變更了。"})


class forget_password(HomeHandler):
    def post(self, *args):
        email = self.params.get_string("email")
        json_data = {}
        if email is u"":
            json_data["email"] = u"請輸入電子信箱"
        if validate_email(email) is False:
            json_data["email"] = u"請電子信箱格式有誤"

        if len(json_data) > 0:
            return self.json(json_data)
        rs = random_string(20)
        member = self.sql.query_one("select * from Member where email = %s", email)
        self.sql.update("Member",{
            "validate_key": rs
        }, {
            "email": email
        })
        url = "http://www.063318866.com/password_sw.html?validate_key=" + rs
        mail_body = u"""

    ＊此信件為系統發出信件，請勿直接回覆，感謝您的配合。謝謝！＊

    親愛的一品夫人會員 %s 您好：

    這封認證信是由一品夫人發出，處理您忘記密碼，
    當您收到此「認證信函」後，
    請直接點選下方連結重新填入新的密碼，無需回信。
    若您

    會員登入
    %s

    如果您有任何問題，
    請您至一品夫人中心官網查詢相關訊息或來信給我們，

    服務電話：(06)3318866
    服務時間：週一～週五 09:00~17:30 例假日除外
    客戶服務信箱：service@063318866.com
    吳氏兄弟開發企業有限公司
    """ % (member["user_name"],url)
        mail.send_mail(sender="service@063318866.com", to=email, subject=u"一品夫人官網訊息通知", body=mail_body)
        return self.json({"done": u"密碼修改信件已經成功送出。"})


class order(MemberMenuHandler):
    def get(self, *args):
        size = self.params.get_integer("size", 10)
        page = self.params.get_integer("page", 1)
        self.page_now = page
        self.page_title = u"訂單查詢"
        if self.current_user is None:
            return self.redirect("/login.html")
        else:
            self.page_all = self.sql.pager('SELECT count(1) FROM OrderInfo Where member_id = %s', self.current_user["id"], size)
            self.order_list = self.sql.query_all('SELECT * FROM OrderInfo Where member_id = %s ORDER BY sort DESC LIMIT %s, %s', (self.current_user["id"], (page - 1) * size, size), (page - 1) * size)
            for item in self.order_list:
                item["link"] = "/order_view.html?id=" + str(item["id"])

class order_view(MemberMenuHandler):
    def get(self, *args):
        id = self.request.get('id') if self.request.get('id') is not None else ''
        if id != '':
            self.record = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', id)
            self.page_title = self.record["order_no"] + u" - 訂單詳細資訊"
            self.order_item_list = self.sql.query_all('SELECT * FROM OrderItem where order_id = %s', id)


class re_question(MemberMenuHandler):
    def get(self, *args):
        if self.current_user is None:
            return self.redirect("/")

        size = self.params.get_integer("size", 5)
        page = self.params.get_integer("page", 1)

        self.page_now = page
        self.page_all = self.sql.pager('SELECT count(1) FROM Guestbook Where member_id = %s', self.current_user["id"], size)
        self.question_list = self.sql.query_all('SELECT * FROM Guestbook Where member_id = %s ORDER BY sort DESC LIMIT %s, %s', (self.current_user["id"], (page - 1) * size, size), (page - 1) * size)


class About(HomeHandler):
    def get(self, *args):
        self.about_list = self.sql.query_all('SELECT * FROM Aboutus where is_enable = 1 and is_delete = 0')
        self.record_id = self.params.get_string("id")
        if self.record_id is u"" or self.record_id is '':
            self.record = self.sql.query_one('SELECT * FROM Aboutus where is_enable = 1 and is_delete = 0')
        else:
            self.record = self.sql.query_one('SELECT * FROM Aboutus where is_enable = 1 and is_delete = 0 and id = %s', self.record_id)


class step01(MemberMenuHandler):
    def get(self, *args):
        self.step_image = "images/step01.gif"
        self.page_title = u"購物清單"
        if "order_id" in self.session:
            id = self.session["order_id"]
            if id != '':
                self.record = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', id)
                self.order_item_list = self.sql.query_all('SELECT * FROM OrderItem where order_id = %s', id)

class step02(MemberMenuHandler):
    def get(self, *args):
        self.step_image = "images/step02.gif"
        self.page_title = u"填寫付款資料"
        self.freighttype_list = self.sql.query_all('SELECT * FROM Freighttype where  is_enable = 1 and is_delete = 0')
        if "order_id" in self.session:
            id = self.session["order_id"]
            if id != '':
                self.record = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', id)

class step02_json(MemberMenuHandler):
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

class step03(MemberMenuHandler):
    def get(self, *args):
        self.step_image = "images/step03.gif"
        self.page_title = u"確認資料"
        if "order_id" in self.session:
            id = self.session["order_id"]
            if id != '':
                self.record = self.sql.query_one('SELECT * FROM OrderInfo where id = %s', id)
                self.order_item_list = self.sql.query_all('SELECT * FROM OrderItem where order_id = %s', id)
            self.total = int(self.record["total_amount"] + self.record["freight"])

class step03_json(MemberMenuHandler):
    def get_new_order_no(self):
        today = datetime.datetime.today() + datetime.timedelta(hours=+8)
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
            d = datetime.datetime.today()
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


class step04(MemberMenuHandler):
    def get(self, *args):
        self.step_image = "images/step04.gif"
        self.page_title = u"訂單完成"

        if "auto_member_account_error" in self.session:
            self.auto_member_account_error = self.session["auto_member_account_error"]
        if "auto_member" in self.session:
            self.auto_member = self.session["auto_member"]
        self.last_order_no = self.session["last_order_no"]

        url = "http://www.063318866.com/admin#/admin/orderinfo/list.html?order_status=1"
        mail_body = u"""

    ＊有一筆新的訂單！＊

    訂購人為 %s
    訂購時間為 %s

    更多詳細內容請至 %s 查看。
    """ % (self.current_user["user_name"],(datetime.datetime.today() + datetime.timedelta(hours=+8)),url)
        mail.send_mail(sender="service@063318866.com", to="service@063318866.com", subject=u"一品夫人官網訂單通知", body=mail_body)

class Error(ProductMenuHandler):
    def get(self, *args):
        pass


class clean_shopping_cart_json(MemberMenuHandler):
    def post(self, *args):
        pass

class add_shopping_cart_json(MemberMenuHandler):
    def post(self, *args):
        today = datetime.datetime.today() + datetime.timedelta(hours=+8)
        product_id = self.params.get_string("product_id")
        quantity = self.params.get_integer("quantity", 0)

        order = None
        if product_id != '':
            product = self.sql.query_one('SELECT * FROM Product where id = %s', product_id)
        else:
            self.json_message(u"產品不存在")
            return
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
            self.json_message(u"remove")
            self.sql.delete("OrderItem", {
                "order_id": order_id,
                "product_id": product_id
            })
        else:
            order_item = self.sql.query_one('SELECT * FROM OrderItem where order_id = %s and product_id = %s', (order_id, product_id))
            if order_item is None:
                self.sql.insert("OrderItem", {
                    "product_id": product_id,
                    "product_no": product["product_no"],
                    "product_name": product["product_name"],
                    "product_price": product["selling_price"],
                    "product_image": product_image,
                    "product_url": "/goods_view.html?parent=1&category=5&id=1",
                    "item_quantity": quantity,
                    "item_status": 0,
                    "item_sum": product["selling_price"] * quantity,
                    "order_id": order_id,
                })
            else:
                self.sql.update("OrderItem", {
                    "item_quantity": quantity,
                    "item_sum": product["selling_price"] * quantity,
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