import os
import webapp2, cgi, sys
import base64,urllib
import json, collections
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Events, Event_LK, Commits
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])

class Home(BaseHandler):
    def get(self):
        template = env.get_template("report.html")
        self.response.write(template.render(name="Overall Reporting", user=BaseHandler.user(self)))

class UserReport(BaseHandler):
    def get(self, user):
        template = env.get_template("report.html")
        user_id = User.query(User.user_id==user).get()
        return_events =  Events.query(Events.user == user_id.key).fetch()
        for data in return_events:
            data.event = Event_LK.query(Event_LK.key == data.event_type).get().event_type
        self.response.write(template.render(name="Individual Reporting", user=BaseHandler.user(self), report = return_events))

class ProjectReport(BaseHandler):
    def get(self, project):
        template = env.get_template("report.html")
        project_id = Project.query(Project.project_id== int(project)).get()
        return_events = Events.query(Events.project == project_id.key).fetch()
        self.response.write(template.render(name="Group Reporting", user=BaseHandler.user(self), events=return_events))

class GetLatestCommits(BaseHandler):
    def get(self, id):
        project_data = Project.query(Project.project_id == int(id)).get()
        project_owner = User.query(User.key == project_data.project_owner).get()
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
                    commit_event = Events(project=project_data.key, user=author.key, event_type=Event_LK.query(Event_LK.event_code == 4).get().key, description=commit['commit']['message'], event_relation_key=commit_key)
                    commit_event.put()
