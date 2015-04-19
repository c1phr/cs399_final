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
        if self.session.get("user") is None:
            self.redirect("/login")
        loaded_projects_user = Project_User.query(Project_User.user_id == self.session.get("user")).fetch()
        if loaded_projects_user is None:
            self.response.write(template.render(name = "Project Overview", project = "{}"))
            return
        list_of_projects = []
        for project in loaded_projects_user:
            Project_stuffs = Project.query(Project.project_id == project.key).fetch()
            get_record = ndb.Key(Project, project.project_id).get()
            # project_data = {"project_title":Project_stuffs.project_title, "project_id":Project_stuffs.project_id,
            #                 "project_desc":Project_stuffs.project_desc, "project_owner":Project_stuffs.project_owner}
            list_of_projects.append(get_record)
        self.response.write(template.render(name = "Project Overview", project = json.dumps(list_of_projects)))