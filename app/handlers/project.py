import os
import webapp2
import json
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

class Project(BaseHandler):
    def get(self, project_id):
        project_data = Project.query(project_id == project_id)

class Loaded(BaseHandler):
    def get(self):
        template = env.get_template("loaded_projects.html")
        user_ids = self.session.get("user")
        if user_ids is None:
            self.redirect("/login")
        loaded_projects_user = Project_User.query(Project_User.user_id == self.session.get("user")).get()
        list_of_projects = []
        if loaded_projects_user is None:
            self.response.write(template.render(name = "Project Overview", project = "{}"))
            return
        for project in loaded_projects_user:
            list_of_projects.append(Project.query(Project.project_id == project.project_id)).get()
        self.response.write(template.render(name = "Project Overview", project = json.dumps(list_of_projects)))