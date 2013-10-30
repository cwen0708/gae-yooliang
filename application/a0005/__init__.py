#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with YooLiang Technology (侑良科技).
# Author: Qi-Liang Wen (温啓良）
# Web: http://www.yooliang.com/
# Date: 2013/9/26
from libs.yooframework import record, image, page
from application.backend import backend, administrator, websetting, webimage, webpage
import marquee, banner, member, partners, home, productcategory, news, faq, product, guestbook, freight, orderinfo, banner2, aboutus
import webapp2

CUSTOMER_NAME = u"YamiYami"
THEME_NAME = u"0005"
DATABASE_NAMESPACE = u"d0005_yamiyami"
CLOUD_SQL_DATABASE = u"d0005_yamiyami"
CLOUD_SQL_INSTANCE_NAME = u"yooliang-technology:database"
CLOUD_STORAGE_BUCKET = u"/template.yooliang.com/"

routes = [
    #==================================================================================================================#
    #前台頁面#
    #==================================================================================================================#
    webapp2.Route('/', handler=home.Index),
    webapp2.Route('/index.html', handler=home.Index),
    webapp2.Route('/about.html', handler=home.About),
    webapp2.Route('/faq.html', handler=home.Faq),
    webapp2.Route('/declare.html', handler=home.Declare),
    webapp2.Route('/process.html', handler=home.Process),
    webapp2.Route('/process02.html', handler=home.Process02),
    webapp2.Route('/contact.html', handler=home.Contact),
    webapp2.Route('/news_list.html', handler=home.NewsList),
    webapp2.Route('/news_view.html', handler=home.NewsView),
    webapp2.Route('/login.html', handler=home.Login),

    webapp2.Route('/goods_list.html', handler=home.goods_list),
    webapp2.Route('/goods_view.html', handler=home.goods_view),
    webapp2.Route('/guestbook.html', handler=home.guestbook),
    webapp2.Route('/guestbook_list.html', handler=home.guestbook_list),
    webapp2.Route('/guestbook_form.html', handler=home.guestbook_form),
    webapp2.Route('/guestbook.json', handler=home.guestbook_json),

    webapp2.Route('/join.html', handler=home.join),
    webapp2.Route('/password.html', handler=home.password),
    webapp2.Route('/password_ch.html', handler=home.password_ch),
    webapp2.Route('/password_sw.html', handler=home.password_sw),
    webapp2.Route('/forget_password.json', handler=home.forget_password),

    webapp2.Route('/info.html', handler=home.info),
    webapp2.Route('/password_ch.html', handler=home.password_ch),
    webapp2.Route('/order.html', handler=home.order),
    webapp2.Route('/order_view.html', handler=home.order_view),
    webapp2.Route('/re_question.html', handler=home.re_question),

    webapp2.Route('/step01.html', handler=home.step01),
    webapp2.Route('/step02.html', handler=home.step02),
    webapp2.Route('/step03.html', handler=home.step03),
    webapp2.Route('/step04.html', handler=home.step04),

    webapp2.Route('/info.json', handler=home.info_json),
    webapp2.Route('/join.json', handler=home.join_json),
    webapp2.Route('/login.json', handler=home.login_json),
    webapp2.Route('/logout.json', handler=home.logout_json),
    webapp2.Route('/step02.json', handler=home.step02_json),
    webapp2.Route('/step03.json', handler=home.step03_json),
    webapp2.Route('/password_ch.json', handler=home.password_ch_json),
    webapp2.Route('/password_sw.json', handler=home.password_sw_json),
    webapp2.Route('/add_shopping_cart.json', handler=home.add_shopping_cart_json),
    webapp2.Route('/clean_shopping_cart.json', handler=home.add_shopping_cart_json),

    webapp2.Route('/error.html', handler=home.Error),

    #==================================================================================================================#
    #後台頁面#
    #==================================================================================================================#
    webapp2.Route('/admin/member/Init.html', handler=member.Init),
    webapp2.Route('/admin/member/list.html', handler=member.List),
    webapp2.Route('/admin/member/create.html', handler=member.Create),
    webapp2.Route('/admin/member/edit.html', handler=member.edit),

    webapp2.Route('/admin/news/init.html', handler=news.Init),
    webapp2.Route('/admin/newscategory/list.html', handler=news.CategoryList),
    webapp2.Route('/admin/newscategory/create.html', handler=news.CategoryCreate),
    webapp2.Route('/admin/newscategory/edit.html', handler=news.CategoryEdit),
    webapp2.Route('/admin/news/list.html', handler=news.List),
    webapp2.Route('/admin/news/create.html', handler=news.Create),
    webapp2.Route('/admin/news/edit.html', handler=news.Edit),

    webapp2.Route('/admin/faq/init.html', handler=faq.Init),
    webapp2.Route('/admin/faqcategory/list.html', handler=faq.CategoryList),
    webapp2.Route('/admin/faqcategory/create.html', handler=faq.CategoryCreate),
    webapp2.Route('/admin/faqcategory/edit.html', handler=faq.CategoryEdit),
    webapp2.Route('/admin/faq/list.html', handler=faq.List),
    webapp2.Route('/admin/faq/create.html', handler=faq.Create),
    webapp2.Route('/admin/faq/edit.html', handler=faq.Edit),

    webapp2.Route('/admin/aboutus/Init.html', handler=aboutus.Init),
    webapp2.Route('/admin/aboutus/list.html', handler=aboutus.List),
    webapp2.Route('/admin/aboutus/create.html', handler=aboutus.Create),
    webapp2.Route('/admin/aboutus/edit.html', handler=aboutus.Edit),

    webapp2.Route('/admin/banner/Init.html', handler=banner.Init),
    webapp2.Route('/admin/banner/list.html', handler=banner.List),
    webapp2.Route('/admin/banner/create.html', handler=banner.Create),
    webapp2.Route('/admin/banner/edit.html', handler=banner.Edit),

    webapp2.Route('/admin/banner2/Buit.html', handler=banner2.Init),
    webapp2.Route('/admin/banner2/list.html', handler=banner2.List),
    webapp2.Route('/admin/banner2/create.html', handler=banner2.Create),
    webapp2.Route('/admin/banner2/edit.html', handler=banner2.Edit),




    webapp2.Route('/admin/guestbook/list.html', handler=guestbook.list),
    webapp2.Route('/admin/guestbook/create.html', handler=guestbook.create),
    webapp2.Route('/admin/guestbook/edit.html', handler=guestbook.edit),

    webapp2.Route('/admin/orderinfo/list.html', handler=orderinfo.list),
    webapp2.Route('/admin/orderinfo/edit.html', handler=orderinfo.edit),
    
    webapp2.Route('/admin/productcategory/list.html', handler=productcategory.list),
    webapp2.Route('/admin/productcategory/create.html', handler=productcategory.create),
    webapp2.Route('/admin/productcategory/edit.html', handler=productcategory.edit),
    
    webapp2.Route('/admin/product/list.html', handler=product.list),
    webapp2.Route('/admin/product/create.html', handler=product.create),
    webapp2.Route('/admin/product/edit.html', handler=product.edit),


    webapp2.Route('/admin/partners/list.html', handler=partners.list),
    webapp2.Route('/admin/partners/create.html', handler=partners.create),
    webapp2.Route('/admin/partners/edit.html', handler=partners.edit),

    webapp2.Route('/admin/marquee/list.html', handler=marquee.list),
    webapp2.Route('/admin/marquee/create.html', handler=marquee.create),
    webapp2.Route('/admin/marquee/edit.html', handler=marquee.edit),

    webapp2.Route('/admin/freight/full_list.html', handler=freight.full_list),
    webapp2.Route('/admin/freighttype/list.html', handler=freight.type_list),
    webapp2.Route('/admin/freighttype/create.html', handler=freight.type_create),
    webapp2.Route('/admin/freighttype/edit.html', handler=freight.type_edit),
    webapp2.Route('/admin/freight/list.html', handler=freight.list),
    webapp2.Route('/admin/freight/create.html', handler=freight.create),
    webapp2.Route('/admin/freight/edit.html', handler=freight.edit),

    
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
    webapp2.Route('/admin/welcome.html', handler=page.admin_page),
    webapp2.Route('/_ah/warmup', handler=page.warmup),
    webapp2.Route('/<:(img|image|images|css|style|js|script|javascript|swf|flash|fla)>/<:(.*)>', handler=page.asserts_file),
    webapp2.Route('/admin/<:(.*)>', handler=page.admin_page),
    webapp2.Route('/<:(.*)>', handler=page.static_page)
]
