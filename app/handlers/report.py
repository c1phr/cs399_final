import os
import webapp2, cgi, sys
import base64,urllib
import json, collections
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Events, Event_LK
from google.appengine.ext import ndb
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])


class Home(BaseHandler):
    def get(self):
        template = env.get_template("report.html")
        project_id = self.request.GET['project']
        user_id = self.request.GET['user']
        num_events = self.request.GET['number'] or 10
        if project_id:
            project_id = ndb.Key(urlsafe=cgi.escape(project_id))
            return_events = Events.query(project=project_id).fetch(num_events)
        elif user_id:
            user_id = ndb.Key(urlsafe=cgi.esacpe(user_id))
            return_events = Events.query(user=user_id).fetch(num_events)
        self.response.write(template.render(name="Issues", user=BaseHandler.user(self), events=return_events))

