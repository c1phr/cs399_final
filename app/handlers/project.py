import os
import webapp2, cgi, sys
import base64
import json, collections
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])


class ProjectDashboard(BaseHandler):
    def get(self, id):
        project_data = Project.query(Project.project_id == int(id)).get()
        template = env.get_template("project_dashboard.html")
        # grab the commits on the project.
        commit_url = "https://api.github.com/repos/" + self.session.get(
            "username") + "/" + project_data.project_title + "/commits?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url=commit_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        commit_contents = json.loads(result.content)

        # grab the languages of the project
        language_url = "https://api.github.com/repos/" + self.session.get(
            "username") + "/" + project_data.project_title + "/languages?access_token=" + self.session.get(
            "access_token")
        result = urlfetch.fetch(url=language_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        language_contents = json.loads(result.content)
        total = 0
        for language in language_contents:
            total += language_contents[language]

        #grab the readme file
        readme_url = "https://api.github.com/repos/" + self.session.get(
            "username") + "/" + project_data.project_title + "/readme?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url=readme_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/vnd.github.3.html"},
                                deadline=10)
        readme_contents = result.content

        team = Project_User.query(Project_User.project_id == project_data.key).fetch()
        user = self.session.get("user")
        team_members = []
        for member in team:
            if member.user_id != user:
                team_member = User.query(User.user_id == member.user_id).get()
                team_members.append(team_member)

        self.response.write(template.render(name="Projects", project_data=project_data,
                                            user=User.query(User.key == self.session.get("user")).get(),
                                            commits=commit_contents, languages=language_contents, total=total,
                                            readme=readme_contents, team=team_members))


class ManageTeam(BaseHandler):
    """
    Post request takes in the project_id of the project that team members are being added for and a complete list of
    new team members. All old team members (except project owner) are deleted and re-added to the datastore.
    """
    def post(self, project_id, team_members):
        team_members = json.loads(team_members)
        project = Project.query(Project.project_id == project_id).get()
        ndb.delete_multi(
            Project_User.query(Project_User.project_id == project.key and not Project_User.is_owner).fetch(
                keys_only=True))
        for member in team_members:
            new_member = Project_User(project_id=project_id, user_id=member)
            new_member.put()


class Loaded(BaseHandler):
    def get(self):
        template = env.get_template("loaded_projects.html")
        if self.session.get("user") is None:
            self.redirect("/login")
        loaded_projects_user = Project_User.query(Project_User.user_id == self.session.get("user")).fetch()
        if loaded_projects_user is None:
            self.response.write(template.render(name="Project Overview", project="{}"))
            return
        list_of_projects = []
        for project in loaded_projects_user:
            project_stuffs = Project.query(Project.key == project.project_id).get()
            list_of_projects.append(project_stuffs)
        self.response.write(template.render(name="Project Overview", project=list_of_projects,
                                            user=User.query(User.key == self.session.get("user")).get()))
