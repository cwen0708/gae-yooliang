#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
from google.appengine.api import memcache


class DBImage(db.Model):
    name = db.StringProperty()
    blob_key = db.StringProperty()

    def url(self):
        import os
        if os.environ.get('HTTP_HOST'):
            url = os.environ['HTTP_HOST']
        else:
            url = os.environ['SERVER_NAME']
        return "http://" + url + '/image/_r/' + self.name + '.png'

class get_upload_json_url(blobstore_handlers.BlobstoreUploadHandler):
    def get(self, *args):
        from google.appengine.ext import blobstore
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        self.response.out.write(blobstore.create_upload_url('/image/upload.json'))

class get_image(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        self.response.headers.add_header(
            'cache-control',
            'public, max-age=604800'
        )
        import urllib
        from google.appengine.ext import blobstore

        img = memcache.get(resource)
        if img is None:
            ds = DBImage.gql("WHERE name = '%s' " % resource).get()
            blob_key = ds.blob_key
            blob_key_2 = str(urllib.unquote(blob_key))
            img = blobstore.BlobInfo.get(blob_key_2)
            if not memcache.add(resource, img, 3600):
                logging.error(u"建立圖片快取時失敗了.")
        self.send_blob(img)

class get_image_by_key(blobstore_handlers.BlobstoreDownloadHandler):
    def get(self, resource):
        import urllib
        from google.appengine.ext import blobstore
        resource = str(urllib.unquote(resource))
        blob_info = blobstore.BlobInfo.get(resource)
        self.send_blob(blob_info)

class upload(blobstore_handlers.BlobstoreUploadHandler):
    def post(self, *args):
        self.response.headers['Content-Type'] = 'text/html; charset=UTF-8'
        import json
        import time
        try:
            upload_files = self.get_uploads('imgFile')
            blob_info = upload_files[0]
            image_url = str(blob_info.key())
            img = DBImage()
            img.blob_key = image_url
            img.name = str((time.time())).replace(".","")
            img.put()
            self.json_data = {"error": 0, "url": img.url()}
        except:
            self.json_data = {"error": 1, "message": "can_not_save_image"}
        json_data = json.dumps(self.json_data)
        self.response.out.write(json_data)