import os
import webapp2
from app.handlers.BaseHandler import BaseHandler
from app.models.models import UserInformation
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))


class MainHandler(BaseHandler):
    def get(self):
        template = env.get_template('index.html')
        self.response.write(template.render(name = "Dashboard", user = UserInformation.query()))

class Project(BaseHandler):
    def get(self):
        template = env.get_template('project.html')
        self.response.write(template.render(name = "Project Overview"))