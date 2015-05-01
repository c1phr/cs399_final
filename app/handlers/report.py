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
        self.response.write(template.render(name="Overall Reporting", user=BaseHandler.user(self)))

class UserReport(BaseHandler):
    def get(self, user):
        template = env.get_template("report.html")
        user_id = User.query(User.user_id==user).get()
        return_events =  Events.query(Events.user == user_id.key).fetch()
        for data in return_events:
            data.event = Event_LK.query(Event_LK.key == data.event_type).get().event_type
        self.response.write(template.render(name="Overall Reporting", user=BaseHandler.user(self), report = return_events))

class ProjectReport(BaseHandler):
    def get(self, project):
        template = env.get_template("report.html")
        project_id = Project.query(Project.project_id== int(project)).get()
        return_events = Events.query(Events.project == project_id.key).fetch()
        #print json.dumps(self.serialize_model(return_events)) # Don't leave me here, I'm for example only!
        self.response.write(template.render(name="Issues", user=BaseHandler.user(self), events=return_events))

