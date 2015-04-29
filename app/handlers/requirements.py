import os
import traceback
from google.appengine.ext import ndb
import webapp2, cgi
import json
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Requirements, Events, Event_LK
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])

# Warning, the methods in this class are untested!
class RequirementsDashboard(BaseHandler):
    def get(self, project_id):
        template = env.get_template("requirements.html")
        project = Project.query(Project.project_id == int(project_id)).get()
        requirements = Requirements.query(Requirements.project_id == project.key, Requirements.active == True).fetch()
        self.response.write(template.render(name = "Requirements",user = BaseHandler.user(self), requirements = requirements, project_id = project_id))

    def put(self, project_id):
        project = Project.query(Project.project_id == int(project_id)).get()
        parent = cgi.escape(self.request.get("parent"))
        description = cgi.escape(self.request.get("description"))
        title = cgi.escape(self.request.get("title"))
        method = cgi.escape(self.request.get("method"))
        if method == "update":
            requirement_id = ndb.Key(urlsafe=cgi.escape(self.request.get("id")))
            requirement = requirement_id.get()
            requirement.req_title = title
            requirement.req_desc = description
            if parent != "None":
                requirement.parent_id = parent
            requirement.put()
        elif method == "delete":
            requirement_id = ndb.Key(urlsafe=cgi.escape(self.request.get("id")))
            requirement = requirement_id.get()
            requirement.active = False
            requirement.put()

        else:
            if parent != "None":
                requirement_id = ndb.Key(urlsafe=cgi.escape(self.request.get("parent")))
                requirement = Requirements(project_id=project.key, req_title=title, req_desc=description, parent_id = requirement_id)
            else:
                requirement = Requirements(project_id=project.key, req_title=title, req_desc=description, parent_id = None)
            try:
                requirement.put()
                self.response.status_int = 200
                self.response.status_message = "Requirement Saved Successfully"
                event = Events(user = BaseHandler.user(self).key, project = project.key, event_type = Event_LK.query(Event_LK.event_code == 3).get().key, description = title + " " + description, event_relation_key = None).put()
            except:
                 self.response.status_int = 500
                 self.response.status_message = traceback.format_exception()
