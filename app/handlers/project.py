import os
import webapp2
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

class Project(BaseHandler):
    def get(self, project_id):
        project_data = Project.query(project_id == project_id)