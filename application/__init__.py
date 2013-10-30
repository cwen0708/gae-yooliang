#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26

RELATIONSHIP = [
    {"app": u"a0005", "name": u"開發環境", "host": u"localhost"},
    {"app": u"a0005", "name": u"測試環境", "host": u"test.yooliang.com"},
    {"app": u"a0005", "name": u"亞米服飾", "host": u"www.yami-yami.com.tw"},
    {"app": u"a0005", "name": u"亞米服飾", "host": u"yami.yooliang.com"},
]

DEBUG = True
APP_CONFIG = {
    'webapp2_extras.sessions': {'secret_key': 'gaesite_sessions'}
}

import webapp2
from webapp2_extras import routes
from google.appengine.ext.appstats import recording

APP_ROUTES = []

# 動態載入路由表
for item in RELATIONSHIP:
    exec "import %s" % item["app"]
    exec('APP_ROUTES += [routes.DomainRoute("' + item["host"] + '", ' + item["app"] + '.routes)]')

app_temp = webapp2.WSGIApplication(APP_ROUTES, debug=DEBUG, config=APP_CONFIG)
app = recording.appstats_wsgi_middleware(app_temp)
