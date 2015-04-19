import os
import webapp2, cgi, sys
import base64
import json, collections
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])


class ProjectDashboard(BaseHandler):
    def get(self, id):
        project_data = Project.query(Project.project_id == int(id)).get()
        template = env.get_template("project_dashboard.html")
        #grab the commits on the project.
        commit_url = "https://api.github.com/repos/" + self.session.get("username") + "/" + project_data.project_title + "/commits?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url = commit_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        commit_contents = json.loads(result.content)

        #grab the languages of the project
        language_url = "https://api.github.com/repos/" + self.session.get("username") + "/" + project_data.project_title + "/languages?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url = language_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        language_contents = json.loads(result.content)
        total = 0
        for language in language_contents:
            total += language_contents[language]

        #grab the readme file
        readme_url = "https://api.github.com/repos/" + self.session.get("username") + "/" + project_data.project_title + "/readme?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url = readme_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/vnd.github.3.html"},
                                deadline=10)
        readme_contents =result.content

        #grab the open current issues on Github
        open_issues_url = "https://api.github.com/repos/" + self.session.get("username") + "/" + project_data.project_title + "/issues?access_token=" + self.session.get("access_token")+"&state=open"
        result = urlfetch.fetch(url = open_issues_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        open_issues_content = json.loads(result.content)
        open_issue = 0
        for issue in open_issues_content:
            open_issue += 1
        #if project_data is None:
           # self.response.write(template.render(name="Invalid Project", project_data="{}", user = User.query(User.key == self.session.get("user")).get()))
        #else:
        self.response.write(template.render(name="Projects", project_data= project_data, user = User.query(User.key == self.session.get("user")).get(), commits = commit_contents, languages = language_contents, total = total, readme = readme_contents, open_issue = open_issue))


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
            Project_stuffs = Project.query(Project.key == project.project_id).get()
            list_of_projects.append(Project_stuffs)
        self.response.write(template.render(name = "Project Overview", project = list_of_projects, user = User.query(User.key == self.session.get("user")).get()))