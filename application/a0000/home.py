#!/usr/bin/env python
# -*- coding: utf-8 -*-
from handler import HomeHandler


class index(HomeHandler):
    def get(self, *args):
        self.nav_current = u"index.html"

class price(HomeHandler):
    def get(self, *args):
        self.nav_current = u"price.html"

class customer(HomeHandler):
    def get(self, *args):
        self.nav_current = u"customer.html"

class protfolio(HomeHandler):
    def get(self, *args):
        self.nav_current = u"protfolio.html"

class contact(HomeHandler):
    def get(self, *args):
        self.nav_current = u"contact.html"

class error(HomeHandler):
    def get(self, *args):
        Here = self
        some = None
        Here.are = some.problems__001
