#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.yooframework.handler import BaseHandler
from application.backend.handler import AdministratorHandler

class warmup(BaseHandler):
    def get(self, *args):
        self.json({"info": u"Warmup"})

class admin_page(AdministratorHandler):
    """ 靜態頁面 """
    def get(self, *args):
        pass

    def post(self, *args):
        pass

class static_page(BaseHandler):
    """ 靜態頁面 """
    def get(self, *args):
        pass

    def post(self, *args):
        pass

class asserts_file(BaseHandler):
    """ 資源檔案 """
    def get(self, folder, url):
        self.redirect("/template/" + self.environ.theme_name + "/" + folder + "/" + url)
        return

    def post(self, folder, url):
        self.redirect("/template/" + self.environ.theme_name + "/" + folder + "/" + url)
        return

class verification_page(BaseHandler):
    def get(self, *args):
        import random
        for i in xrange(1, 6):
            self.session["verification_code_" + str(i)] = chr(random.randint(48,57))
        self.m1 = random.randint(0,100)
        self.m2 = random.randint(0,100)
        self.m3 = random.randint(0,100)
        self.m4 = random.randint(0,100)
        self.m5 = random.randint(0,100)
        self.render("/verification_code/page.html", "zoo")

class verification_code(BaseHandler):
    def get(self, position, *args):
        import random
        self.redirect("/static/plugins/verification_code/s" + str(random.randint(1,5)) + "/" + self.session["verification_code_" + position] + ".png?r=" + str(random.randint(1,100)))

class insert_data(BaseHandler):
    def get(self, *args):
        """
        try:
            from google.appengine.api import rdbms

            conn = rdbms.connect(instance=_INSTANCE_NAME, database='guestbook')
            cursor = conn.cursor()
            cursor.execute('SELECT guestName, content, entryID FROM entries')
            self.list = cursor.fetchall()
        except:
            pass
        """
        try:
            from google.appengine.api import rdbms
            conn = rdbms.connect(instance="_INSTANCE_NAME", database='guestbook')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO entries (guestName, content) VALUES (%s, %s)', ('aaa', 'bbb'))
            conn.commit()
            conn.close()
        except:
            pass
