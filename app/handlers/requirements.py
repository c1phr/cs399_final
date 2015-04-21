import os
import traceback
import webapp2, cgi
import json
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Requirements
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])

# Warning, the methods in this class are untested!
class RequirementsDashboard(BaseHandler):
    def get(self, project_id):
        requirements = Requirements.query(Requirements.project_id == project_id)
        # This can be changed as we create the template for requirements, leaving it here for testing
        return json.dumps(requirements)

    def put(self, project_id):
        parent = cgi.escape(self.request.get("parent"))
        description = cgi.escape(self.request.get("description"))
        title = cgi.escape(self.request.get("title"))
        requirement = Requirements(project_id=int(project_id), req_title=title, req_desc=description, parent_id=parent)
        try:
            requirement.put()
            self.response.status_int = 200
            self.response.status_message = "Requirement Saved Successfully"
        except:
            self.response.status_int = 500
            self.response.status_message = traceback.format_exception()

    def delete(self, requirement_id):
        requirement = Requirements(Requirements.key == requirement_id)
        try:
            requirement.key.delete()
            self.response.status_int = 200
            self.response.status_message = "Requirement Deleted Successfully"
        except:
            self.response.status_int = 500
            self.response.status_message = traceback.format_exception()

    def update(self, requirement_id):
        requirement = Requirements(Requirements.key == requirement_id)
        parent = cgi.escape(self.request.get("parent"))
        description = cgi.escape(self.request.get("description"))
        title = cgi.escape(self.request.get("title"))
        requirement.parent_id = parent
        requirement.req_desc = description
        requirement.req_title = title
        try:
            requirement.put()
            self.response.status_int = 200
            self.response.status_message = "Requirement Updated Successfully"
        except:
            self.response.status_int = 500
            self.response.status_message = traceback.format_exception()