import os
import webapp2, cgi, sys
import base64,urllib
import json, collections
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])


class Home(BaseHandler):
    def get(self):
        template = env.get_template("report.html")
        self.response.write(template.render(name="Issues", user = BaseHandler.user(self)))

