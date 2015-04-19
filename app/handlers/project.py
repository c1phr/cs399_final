import os
import webapp2, cgi
import json
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

class ProjectDashboard(BaseHandler):
    def get(self, id):
        project_data = Project.query(Project.project_id == int(id)).get()
        template = env.get_template("project_dashboard.html")
        commit_url = "https://api.github.com/repos/" + self.session.get("username") + "/" + project_data.project_title + "/commits?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url = commit_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        commit_contents = json.loads(result.content)

        #if project_data is None:
           # self.response.write(template.render(name="Invalid Project", project_data="{}", user = User.query(User.key == self.session.get("user")).get()))
        #else:
        self.response.write(template.render(name="Projects", project_data= project_data, user = User.query(User.key == self.session.get("user")).get(), commits = commit_contents))

class Loaded(BaseHandler):
    def get(self):
        template = env.get_template("loaded_projects.html")
        user_ids = self.session.get("user")
        if user_ids is None:
            self.redirect("/login")
        loaded_projects_user = Project_User.query(Project_User.user_id == self.session.get("user")).fetch()
        list_of_projects = []
        if loaded_projects_user is None:
            self.response.write(template.render(name = "Project Overview", project = "{}"))
            return
        for project in loaded_projects_user:
            list_of_projects.append(Project.query(Project.key == project.key).get())
        self.response.write(template.render(name = "Project Overview", project = json.dumps(list_of_projects)))