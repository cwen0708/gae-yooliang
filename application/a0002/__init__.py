#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26
from libs.yooframework import record, image, page
from application.backend import backend, administrator, websetting, webimage, webpage
import marquee, banner, home, productcategory, news, faq, product, contact, statuscode, aboutus
import solution, service, rawdata, customer, caseinfo, equipment, monitor, contact2
import webapp2

CUSTOMER_NAME = u"牧陽能控有限公司"
THEME_NAME = u"0002"
DATABASE_NAMESPACE = u"greenshepherd"
CLOUD_SQL_DATABASE = u"greenshepherd"
CLOUD_SQL_INSTANCE_NAME = u"greenshepherd.com.tw:greenshepherd:greenshepherd"
CLOUD_STORAGE_BUCKET = u""

routes = [

    #==================================================================================================================#
    #前台頁面#
    #==================================================================================================================#
    webapp2.Route('/', home.index),
    webapp2.Route('/index.html', home.index),
    webapp2.Route('/about.html', home.about),
    webapp2.Route('/solution.html', home.solution),
    webapp2.Route('/solution_view.html', home.solution_view),

    webapp2.Route('/login.html', home.login),
    webapp2.Route('/service.html', home.service),
    webapp2.Route('/bcastr.xml', home.bcastr),

    webapp2.Route('/learn.html', home.learn),
    webapp2.Route('/learn_view.html', home.learn_view),
    webapp2.Route('/product.html', home.product),
    webapp2.Route('/product_view.html', home.product_view),
    webapp2.Route('/project.html', home.project),
    webapp2.Route('/project_detail.html', home.project_detail),
    webapp2.Route('/contact_step_1.html', home.contact_step_1),
    webapp2.Route('/contact_step_2-1.html', home.contact_step_2_1),
    webapp2.Route('/contact_step_2-2.html', home.contact_step_2_2),
    webapp2.Route('/contact_step_2-3.html', home.contact_step_2_3),
    webapp2.Route('/contact_step_2-4.html', home.contact_step_2_4),
    webapp2.Route('/contact_step_2-5.html', home.contact_step_2_5),
    webapp2.Route('/contact_step_3.html', home.contact_step_3),
    webapp2.Route('/contact_step_4.html', home.contact_step_4),
    webapp2.Route('/contact_step_5.html', home.contact_step_5),
    webapp2.Route('/contact.html', home.contact),

    webapp2.Route('/send_contact_info.json', home.send_contact_info),

    webapp2.Route('/data/status', home.data_equipment_status),
    webapp2.Route('/data/insert', home.data_insert),
    webapp2.Route('/monitor.html', home.monitor),
    webapp2.Route('/monitor_info.html', home.monitor_info),
    webapp2.Route('/monitor_realtime.html', home.monitor_realtime),
    webapp2.Route('/monitor_frame_1.html', home.monitor_frame_1),
    webapp2.Route('/monitor_frame_2.html', home.monitor_frame_2),
    webapp2.Route('/monitor_detail_week.html', home.monitor_detail_week),
    webapp2.Route('/monitor_detail_month.html', home.monitor_detail_month),
    webapp2.Route('/monitor_detail_year.html', home.monitor_detail_year),
    webapp2.Route('/check_update', home.check_update),
    webapp2.Route('/project_flickr.html', home.project_flickr),


    webapp2.Route('/error.html', home.error),
    webapp2.Route('/user_login', home.user_login),
    webapp2.Route('/user_logout', home.user_logout),

    webapp2.Route('/watermark.png', home.watermark),


    #==================================================================================================================#
    #後台頁面#
    #==================================================================================================================#
    webapp2.Route('/admin/faqcategory/list.html', handler=faq.category_list),
    webapp2.Route('/admin/faqcategory/create.html', handler=faq.category_create),
    webapp2.Route('/admin/faqcategory/edit.html', handler=faq.category_edit),
    webapp2.Route('/admin/faq/list.html', handler=faq.list),
    webapp2.Route('/admin/faq/create.html', handler=faq.create),
    webapp2.Route('/admin/faq/edit.html', handler=faq.edit),

    webapp2.Route('/admin/contact2/init', handler=contact2.Init),
    webapp2.Route('/admin/contact2/list.html', handler=contact2.List),
    webapp2.Route('/admin/contact2/edit.html', handler=contact2.Edit),
    webapp2.Route('/admin/contact/list.html', handler=contact.list),
    webapp2.Route('/admin/contact/edit.html', handler=contact.edit),

    webapp2.Route('/admin/monitor/list.html', handler=monitor.List),
    webapp2.Route('/admin/monitor/edit.html', handler=monitor.List),

    webapp2.Route('/admin/statuscode/list.html', handler=statuscode.list),
    webapp2.Route('/admin/statuscode/create.html', handler=statuscode.create),
    webapp2.Route('/admin/statuscode/edit.html', handler=statuscode.edit),

    webapp2.Route('/admin/websetting/list.html', handler=websetting.list),
    webapp2.Route('/admin/websetting/create.html', handler=websetting.create),
    webapp2.Route('/admin/websetting/edit.html', handler=websetting.edit),

    webapp2.Route('/admin/news/list.html', handler=news.list),
    webapp2.Route('/admin/news/create.html', handler=news.create),
    webapp2.Route('/admin/news/edit.html', handler=news.edit),

    webapp2.Route('/admin/aboutus/list.html', handler=aboutus.List),
    webapp2.Route('/admin/aboutus/create.html', handler=aboutus.Create),
    webapp2.Route('/admin/aboutus/edit.html', handler=aboutus.Edit),

    webapp2.Route('/admin/banner/list.html', handler=banner.List),
    webapp2.Route('/admin/banner/create.html', handler=banner.Create),
    webapp2.Route('/admin/banner/edit.html', handler=banner.Edit),

    webapp2.Route('/admin/solution/list.html', handler=solution.List),
    webapp2.Route('/admin/solution/create.html', handler=solution.Create),
    webapp2.Route('/admin/solution/edit.html', handler=solution.Edit),

    webapp2.Route('/admin/webpage/list.html', handler=webpage.list),
    webapp2.Route('/admin/webpage/create.html', handler=webpage.create),
    webapp2.Route('/admin/webpage/edit.html', handler=webpage.edit),

    webapp2.Route('/admin/service/list.html', handler=service.list),
    webapp2.Route('/admin/service/create.html', handler=service.create),
    webapp2.Route('/admin/service/edit.html', handler=service.edit),

    webapp2.Route('/admin/rawdata/list.html', handler=rawdata.list),
    webapp2.Route('/admin/rawdata/create.html', handler=rawdata.create),
    webapp2.Route('/admin/rawdata/edit.html', handler=rawdata.edit),

    webapp2.Route('/admin/customer/list.html', handler=customer.list),
    webapp2.Route('/admin/customer/create.html', handler=customer.create),
    webapp2.Route('/admin/customer/edit.html', handler=customer.edit),

    webapp2.Route('/admin/caseinfo/list.html', handler=caseinfo.List),
    webapp2.Route('/admin/caseinfo/create.html', handler=caseinfo.create),
    webapp2.Route('/admin/caseinfo/edit.html', handler=caseinfo.edit),

    webapp2.Route('/admin/equipment/list.html', handler=equipment.list),
    webapp2.Route('/admin/equipment/create.html', handler=equipment.create),
    webapp2.Route('/admin/equipment/edit.html', handler=equipment.edit),

    webapp2.Route('/admin/marquee/list.html', handler=marquee.list),
    webapp2.Route('/admin/marquee/create.html', handler=marquee.create),
    webapp2.Route('/admin/marquee/edit.html', handler=marquee.edit),

    webapp2.Route('/admin/product/list.html', handler=product.list),
    webapp2.Route('/admin/product/create.html', handler=product.create),
    webapp2.Route('/admin/product/edit.html', handler=product.edit),

    webapp2.Route('/admin/productcategory/list.html', handler=productcategory.list),
    webapp2.Route('/admin/productcategory/create.html', handler=productcategory.create),
    webapp2.Route('/admin/productcategory/edit.html', handler=productcategory.edit),
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
