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


class Home(BaseHandler):
    def get(self, id):
        template = env.get_template("issues.html")
        open_issues_url = "https://api.github.com/repos/" + self.session.get(
            "username") + "/" + cgi.escape(id) + "/issues?access_token=" + self.session.get(
            "access_token") + "&state=open"
        result = urlfetch.fetch(url=open_issues_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        open_issues_content = json.loads(result.content)
        self.response.write(template.render(name="Issues",open_issues = open_issues_content,
                                            user=User.query(User.key == self.session.get("user")).get(), project = cgi.escape(id)))