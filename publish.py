#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import os
import urllib2

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'])

class PublishHandler(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            user_name = user.nickname()
            logout_url = users.create_logout_url(self.request.uri)
            url_linktext = 'Logout'
        else:
            self.redirect(users.create_login_url('/publish'))
            return
        
        template_values = {
            'page': 'publish',
            'user_name': user_name,
            'logout_url': logout_url,
        }
        template = JINJA_ENVIRONMENT.get_template('publish.html')
        self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
    ('/publish', PublishHandler),
], debug=True)
