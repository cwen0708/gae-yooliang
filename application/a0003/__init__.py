#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26
from libs.yooframework import record, image, page
from application.backend import backend, administrator, websetting, webimage, webpage
from application.a0003 import home, pastcase, hotcase
import webapp2

CUSTOMER_NAME = u"全日昇建設"
THEME_NAME = u"0003"
DATABASE_NAMESPACE = u"d0003_crsconstruction"
CLOUD_SQL_DATABASE = u"d0003_crsconstruction"
CLOUD_SQL_INSTANCE_NAME = u"yooliang-technology:database"
CLOUD_STORAGE_BUCKET = u"/template.yooliang.com/"

routes = [
    #==================================================================================================================#
    #前台頁面#
    #==================================================================================================================#
    webapp2.Route('/', handler=home.Index),
    webapp2.Route('/index.html', handler=home.Index),
    webapp2.Route('/about.html', handler=home.About),
    webapp2.Route('/contact.html', handler=home.Contact),
    webapp2.Route('/case_list.html', handler=home.CaseList),
    webapp2.Route('/case_view.html', handler=home.CaseView),
    webapp2.Route('/hot_list.html', handler=home.HotList),
    webapp2.Route('/hot_view.html', handler=home.HotView),

    #==================================================================================================================#
    #後台頁面#
    #==================================================================================================================#
    webapp2.Route('/admin/pastcase/init.html', handler=pastcase.Init),
    webapp2.Route('/admin/pastcase/list.html', handler=pastcase.List),
    webapp2.Route('/admin/pastcase/create.html', handler=pastcase.Create),
    webapp2.Route('/admin/pastcase/edit.html', handler=pastcase.Edit),
    
    webapp2.Route('/admin/hotcase/init.html', handler=hotcase.Init),
    webapp2.Route('/admin/hotcase/list.html', handler=hotcase.List),
    webapp2.Route('/admin/hotcase/create.html', handler=hotcase.Create),
    webapp2.Route('/admin/hotcase/edit.html', handler=hotcase.Edit),

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
