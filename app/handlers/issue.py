import os
import webapp2, cgi, sys
import base64,urllib
import json, collections
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Project_User
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])


class Home(BaseHandler):
    def get(self, id):
        template = env.get_template("issues.html")
        project = Project.query(Project.project_title == cgi.escape(id)).get()
        project_owner = User.query(User.key == project.project_owner).get()

        open_issues_url = "https://api.github.com/repos/" +  project_owner.user_id + "/" + cgi.escape(id) + "/issues?access_token=" + self.session.get(
            "access_token") + "&state=open"
        result = urlfetch.fetch(url=open_issues_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        open_issues_content = json.loads(result.content)

        #closed issues
        closed_issues_url = "https://api.github.com/repos/" +  project_owner.user_id + "/" + cgi.escape(id) + "/issues?access_token=" + self.session.get(
            "access_token") + "&state=closed"
        result = urlfetch.fetch(url=closed_issues_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        closed_issues_content = json.loads(result.content)
        self.response.write(template.render(name="Issues",open_issues = open_issues_content,closed_issues = closed_issues_content,
                                            user=BaseHandler.user(self), project = project.project_id, project_name = project.project_title, owner = project_owner.user_id))



class CloseIssue(BaseHandler):
    def post(self):
        issue_id = cgi.escape(self.request.get('issue_id'))
        issue_title = cgi.escape(self.request.get('issue_title'))
        issue_body = cgi.escape(self.request.get('issue_body'))
        issue_milestone = cgi.escape(self.request.get('issue_milestone'))
        issue_assignee = cgi.escape(self.request.get('issue_assignee'))
        project = cgi.escape(self.request.get('project'))
        data_vals = {"title" : issue_title,
                     "body": issue_body,
                     "assignee": issue_assignee,
                     "state" : "closed",
                     "milestone" : issue_milestone,
                     "labels": ([])}
        data = urllib.urlencode(data_vals)
        open_issues_url = "https://api.github.com/repos/" +  BaseHandler.user_id(self) + "/" + project + "/issues/" + issue_id + "?access_token=" + self.session.get("access_token")
        result = urlfetch.fetch(url=open_issues_url,
                                payload=data,
                                method=urlfetch.PATCH,
                                headers={"Accept": "application/json"},
                                deadline=10)
        #open_issues_content = json.loads(result.content)