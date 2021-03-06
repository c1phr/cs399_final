import os
from datetime import datetime
from google.appengine.ext import ndb
import webapp2, cgi
import json
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User, Requirements, Events, Event_LK, Commits
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])


class Events_LK(object):
    pass


class ProjectDashboard(BaseHandler):
    def get(self, id):
        user_id = BaseHandler.user_id(self)
        if not self.session.get("user"):
            self.redirect("/")
        project_data = Project.query(Project.project_id == int(id)).get()
        template = env.get_template("project_dashboard.html")
        project_owner = User.query(User.key == project_data.project_owner).get()
        if self.session.get("user") is None:
            self.redirect("/login")
        username = User.query(User.key == self.session.get("user"))
        # grab the commits on the project.
        commit_url = "https://api.github.com/repos/" + project_owner.user_id + "/" + project_data.project_title + "/commits?access_token=" + self.session.get(
            "access_token")
        result = urlfetch.fetch(url=commit_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        commit_contents = json.loads(result.content)
        for commit in commit_contents:
            if not Commits.query(Commits.sha == commit['sha']).fetch(1):
                author = User.query(User.user_id == commit['committer']['login']).get()
                if author: # Only store commits for our team
                    new_commit = Commits(sha=commit['sha'], message=commit['commit']['message'], author=author.key, project=project_data.key)
                    commit_key = new_commit.put()
                    commit_time = datetime.strptime(commit['commit']['author']['date'], "%Y-%m-%dT%H:%M:%SZ")
                    commit_event = Events(timestamp=commit_time,project=project_data.key, user=author.key, event_type=Event_LK.query(Event_LK.event_code == 4).get().key, description=commit['commit']['message'], event_relation_key=commit_key)
                    commit_event.put()

        # grab the languages of the project
        language_url = "https://api.github.com/repos/" + project_owner.user_id + "/" + project_data.project_title + "/languages?access_token=" + self.session.get(
            "access_token")
        result = urlfetch.fetch(url=language_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        language_contents = json.loads(result.content)
        total = 0
        for language in language_contents:
            total += language_contents[language]

        # grab the readme file
        readme_url = "https://api.github.com/repos/" + project_owner.user_id + "/" + project_data.project_title + "/readme?access_token=" + self.session.get(
            "access_token")
        result = urlfetch.fetch(url=readme_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/vnd.github.3.html"},
                                deadline=10)
        readme_contents = result.content


        # grab the open current issues on Github
        open_issues_url = "https://api.github.com/repos/" + project_owner.user_id + "/" + project_data.project_title + "/issues?access_token=" + self.session.get(
            "access_token") + "&state=open"
        result = urlfetch.fetch(url=open_issues_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        open_issues_content = json.loads(result.content)
        open_issue = 0
        for issue in open_issues_content:
            open_issue += 1

        team = Project_User.query(Project_User.project_id == project_data.key).fetch()
        user = self.session.get("user")
        team_members = []
        for member in team:
            if member.user_id != user:
                team_member = User.query(User.key == member.user_id).get()
                team_members.append(team_member)

        self.response.write(template.render(name="Projects", project_data=project_data,
                                            user=BaseHandler.user(self),
                                            commits=commit_contents, languages=language_contents, total=total,
                                            readme=readme_contents, open_issue=open_issue, team=team_members,
                                            owner=project_owner.user_id))


class ManageTeam(BaseHandler):
    def post(self):
        project_id = int(cgi.escape(self.request.get('project_id')))
        username = cgi.escape(self.request.get('username'))
        method = cgi.escape(self.request.get('method'))
        project = Project.query(Project.project_id == project_id).get()
        if method == "delete":
            old_user = User.query(User.user_id == username).get()
            old_member = Project_User.query(
                Project_User.project_id == project.key and Project_User.user_id == old_user.key).get()
            old_member.key.delete()
            event_message = username + " was deleted from " + project.project_title + " by " + self.user().user_id

        elif method == "put":
            new_user = User.query(User.user_id == username).get()
            new_member = Project_User(project_id=project.key, user_id=new_user.key)
            new_member.put()
            event_message = username + " was added to " + project.project_title + " by " + self.user().user_id

        event = Events(project=project.key,
                       user=self.user().key,
                       event_type=Event_LK.query(Event_LK.event_code == 5).get().key,
                       description=event_message,
                       event_relation_key=None)
        event.put()


class Loaded(BaseHandler):
    def get(self):
        template = env.get_template("loaded_projects.html")
        if self.session.get("user") is None:
            return self.redirect("/login")
        loaded_projects_user = Project_User.query(Project_User.user_id == self.session.get("user")).fetch()
        if loaded_projects_user is None:
            self.response.write(template.render(name="Project Overview", project="{}"))
            return
        list_of_projects = []
        for project in loaded_projects_user:
            project_stuffs = Project.query(Project.key == project.project_id).get()
            list_of_projects.append(project_stuffs)
        self.response.write(template.render(name="Project Overview",
                                            project=list_of_projects,
                                            user=BaseHandler.user(self)))
