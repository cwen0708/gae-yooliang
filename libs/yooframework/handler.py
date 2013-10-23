#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import webapp2
import jinja2
from environmentinfo import EnvironmentInfo
from config import ConfigInfo
from param import ParamInfo
from google.appengine.api import namespace_manager
from webapp2_extras import sessions
from database import CloudSQL
from storage import CloudStorage


class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request=None, response=None):
        self.environ = EnvironmentInfo()
        self.config = ConfigInfo()
        self.params = ParamInfo(request)
        if self.environ.host == "localhost":
            self.is_localhost = True
            sql_user = "root"
            sql_password = "1234"
        else:
            self.is_localhost = False
            sql_user = None
            sql_password = None
        self.sql = CloudSQL(self.environ.cloud_sql_instance_name, self.environ.cloud_sql_database_name, sql_user, sql_password)
        self.storage = CloudStorage(self.environ.cloud_storage_bucket_name)
        self.app_version = self.environ.app_version
        self.session_store = sessions.get_store(request=request)
        self.app_init()
        super(BaseHandler, self).__init__(request, response)
        if self.config.redirect_url != u"":
            self.redirect(self.config.redirect_url)
        #namespace_manager.set_namespace(EnvironmentInfo.get_namespace())

    def app_init(self):
        pass

    def page_init(self):
        pass

    def before_dispatch(self):
        self.page_init()

    def after_dispatch(self):
        pass

    def redirect(self, uri, permanent=False, abort=False, code=None, body=None):
        self.environ.template_already_render = True
        self.config.redirect_url = uri
        super(BaseHandler, self).redirect(uri)

    def dispatch(self):
        self.before_dispatch()
        super(BaseHandler, self).dispatch()
        self.after_dispatch()
        self.session_store.save_sessions(self.response)
        if self.environ.template_already_render is False:
            self.render(None)

    @webapp2.cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def get_int_param(self, key="size", default_value=0):
        try:
            if self.request.get(key) is None:
                return default_value
            _a = self.request.get(key) if int(self.request.get(key)) is not None else u''
            return default_value if _a == '' else int(_a)
        except:
            return default_value

    def json_message(self, info):
        if self.environ.template_already_render is False:
            self.json({"info": info})

    def json(self,data):
        json_data_o = data
        import json
        json_data = json.dumps(json_data_o)
        self.response.out.write(json_data)
        self.environ.template_already_render = True
        return

    def render(self, url, theme=None):
        if self.environ.template_already_render:
            return
        self.environ.template_already_render = True
        url = self.request.path[1:] if url is None else url
        url = url[1:] if url.startswith('/') else url
        url_file = 'index' if os.path.basename(url.split('?')[0]) == '' else os.path.basename(url.split('?')[0])
        url_file = url_file + '.html' if os.path.splitext(url_file)[1] == '' else url_file
        url_path = '' if url_file == os.path.dirname(url.split('?')[0]) else os.path.dirname(url.split('?')[0])

        if self.config.template_render_from_cloud_storage:
            self.render_by_cloud_storage(url_path, url_file, theme)
        else:
            self.render_by_physical_file(url_path, url_file, theme)

    def __handle_exception(self, exception, debug):
        """ 自定義錯誤頁面 """
        import traceback
        import sys
        self.response.status = 500
        self.error_msg = ''.join(traceback.format_exception(*sys.exc_info()))
        self.render_by_physical_file('system', 'default_error.html')

    def get_webimage(self, value):
        r = self.sql.query_one('SELECT value FROM WebImage where setting_no = %s', value)
        if r is not None:
            return r["value"]
        else:
            return ""

    def get_webpage(self, value):
        r = self.sql.query_one('SELECT value FROM WebPage where setting_no = %s', value)
        if r is not None:
            return r["value"]
        else:
            return u""

    def get_websetting(self, value):
        r = self.sql.query_one('SELECT value FROM WebSetting where setting_no = %s', value)
        if r is not None:
            return r["value"]
        else:
            return u""

    def jinja2_loader(self, loader):
        template_environment = jinja2.Environment(loader=loader)

        def get_webimage(value):
            return self.get_webimage(value)

        def get_webpage(value):
            return self.get_webpage(value)

        def get_websetting(value):
            return self.get_websetting(value)

        def thousands_separator(value):
            return format(int(value),',')

        def website_url(value):
            value = str(value)
            if value[0:1] == "/":
                rp = ""
            else:
                rp = "/"
            return self.environ.base_url + rp + value

        from libs.yooframework.filters import datetime_format, static_path, datetime_timesp
        template_environment.filters['datetime_format'] = datetime_format
        template_environment.filters['datetime_timesp'] = datetime_timesp
        template_environment.filters['webimage'] = get_webimage
        template_environment.filters['websetting'] = get_websetting
        template_environment.filters['webpage'] = get_webpage
        template_environment.filters['thousands_separator'] = thousands_separator
        template_environment.filters['static_path'] = static_path
        template_environment.filters['url'] = website_url
        return template_environment

    def render_by_cloud_storage(self, path, template_file, theme=None):
        if theme is None:
            theme = self.environ.theme_name
        path = "/" + theme + "/" + path + "/" + template_file
        base_path = "/" + theme + "/base.html"
        from jinja2 import DictLoader
        loader = DictLoader({
            'base.html': (self.storage.read_file(base_path)).read().decode('utf-8'),
            template_file: (self.storage.read_file(path)).read().decode('utf-8')
        })
        template_environment = self.jinja2_loader(loader)
        template = template_environment.get_template(template_file, path)
        response_out_text = template.render(self.__dict__)
        self.environ.template_already_render = True
        self.response.out.write(response_out_text)

    def render_by_physical_file(self, path, template_file, theme=None):
        """ 從實體路徑渲染 """
        if theme is None:
            theme = self.environ.theme_name
        template_path = os.path.join(self.environ.template_root , theme)
        template_path_sys = os.path.join(template_path, "system")
        template_path_temp = template_path
        template_path_list = [template_path, template_path_sys]
        for item in path.split("/"):
            template_path_temp = os.path.join(template_path_temp, item)
            template_path_list.append(template_path_temp)

        if os.path.exists(os.path.join(template_path_temp, template_file)):
            pass
        elif os.path.exists(os.path.join(template_path_sys, "not_found.html")):
            self.error_msg = os.path.join(template_path_temp, template_file)
            self.error_msg = self.error_msg.split("template")[1]
            self.error(404)
            template_file = "not_found.html"
        else:
            self.error_msg = os.path.join(template_path_temp, template_file)
            self.error_msg = self.error_msg.split("template")[1]
            self.error(404)
            template_file = "not_found.html"
            theme = "system"
            template_path = os.path.join(self.environ.template_root, theme)
            template_path_list = [template_path]

        loader = jinja2.FileSystemLoader(template_path_list)
        template_environment = self.jinja2_loader(loader)

        template = template_environment.get_template(template_file, path)
        response_out_text = template.render(self.__dict__)
        self.environ.template_already_render = True
        self.response.out.write(response_out_text)

