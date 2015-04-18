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


class MainHandler(BaseHandler):
    def get(self):
        template = env.get_template('index.html')
        #self.response.write(template.render(name = "Dashboard", user = User.query(), token = self.session.get("access_token")))
        self.response.write(template.render(name = "Dashboard", token = self.session.get("access_token")))

class Register(BaseHandler):
    def get(self):
        template = env.get_template("registration.html")
        self.response.write(template.render(name = "Registration"))

    def post(self):
        first = cgi.escape(self.request.get('first'))
        last = cgi.escape(self.request.get('last'))
        email = cgi.escape(self.request.get('email'))
        person = User(user_id=%%%, first_name=first, last_name=last, email=email)
        person.put()

class Project(BaseHandler):
    def get(self):
        access_url = "https://api.github.com/user/repos?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url = access_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        project_contents = json.loads(result.content)
        template = env.get_template('project.html')
        self.response.write(template.render(name = "Project Overview", project = project_contents))
