import os
import webapp2
from app.handlers.BaseHandler import BaseHandler
import cgi, urllib, json
from google.appengine.api import urlfetch
from secrets import secrets
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))


class Information(BaseHandler):
    def get(self, username):
        clean_username = cgi.escape(username)
        user = User.query(User.user_id == clean_username).get()
        template = env.get_template('user.html')
        self.response.write(template.render(name = "User Information", user = user))
