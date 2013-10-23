#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.yooframework import record, image, page
from application.backend import backend, administrator, websetting, webimage, webpage
import home
import webapp2
CUSTOMER_NAME = u"侑良科技"
THEME_NAME = u"0000"
DATABASE_NAMESPACE = u"d0000_yooliang"
CLOUD_SQL_DATABASE = u"d0000_yooliang"
CLOUD_SQL_INSTANCE_NAME = u"yooliang-technology:database"
CLOUD_STORAGE_BUCKET = u"/template.yooliang.com/"

routes = [
    webapp2.Route('/', handler=home.index),
    #==================================================================================================================#
    #前台頁面#
    #==================================================================================================================#
    webapp2.Route('/index.html', handler=home.index),
    webapp2.Route('/error.html', handler=home.error),
    webapp2.Route('/price.html', handler=home.price),
    webapp2.Route('/contact.html', handler=home.contact),
    webapp2.Route('/customer.html', handler=home.customer),
    webapp2.Route('/protfolio.html', handler=home.protfolio),

    #==================================================================================================================#
    #後台頁面#
    #==================================================================================================================#

    #==================================================================================================================#
    #通用頁面#
    #==================================================================================================================#
    webapp2.Route('/admin', handler=backend.init),
    webapp2.Route('/admin/logout.html', handler=backend.logout),
    webapp2.Route('/admin/login_jump.html', handler=backend.login_jump),
    webapp2.Route('/admin/login.html', handler=backend.login),
    webapp2.Route('/admin/record/delete.json', handler=record.delete),
    webapp2.Route('/admin/record/real_delete.json', handler=record.real_delete),
    webapp2.Route('/admin/record/enable.json', handler=record.enable),
    webapp2.Route('/admin/record/disable.json', handler=record.disable),
    webapp2.Route('/admin/record/recovery.json', handler=record.recovery),
    webapp2.Route('/admin/record/sort.json', handler=record.sort),
    webapp2.Route('/admin/administrator/list.html', handler=administrator.list),
    webapp2.Route('/admin/administrator/create.html', handler=administrator.create),
    webapp2.Route('/admin/administrator/edit.html', handler=administrator.edit),
    webapp2.Route('/admin/webimage/list.html', handler=webimage.list),
    webapp2.Route('/admin/webimage/create.html', handler=webimage.create),
    webapp2.Route('/admin/webimage/edit.html', handler=webimage.edit),
    webapp2.Route('/admin/webpage/list.html', handler=webpage.list),
    webapp2.Route('/admin/webpage/create.html', handler=webpage.create),
    webapp2.Route('/admin/webpage/edit.html', handler=webpage.edit),
    webapp2.Route('/admin/websetting/list.html', handler=websetting.list),
    webapp2.Route('/admin/websetting/create.html', handler=websetting.create),
    webapp2.Route('/admin/websetting/edit.html', handler=websetting.edit),
    webapp2.Route('/_ah/warmup', handler=page.warmup),
    webapp2.Route('/<:(img|image|images|css|style|js|script|javascript|swf|flash|fla)>/<:(.*)>', handler=page.asserts_file),
    webapp2.Route('/admin/<:(.*)>', handler=page.admin_page),
    webapp2.Route('/<:(.*)>', handler=page.static_page)
]
