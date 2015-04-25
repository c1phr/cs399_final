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
        template = env.get_template("requirements.html")
        project = Project.query(Project.project_id == int(project_id)).get()
        requirements = Requirements.query(Requirements.project_id == project.key).fetch()
        # This can be changed as we create the template for requirements, leaving it here for testing
        self.response.write(template.render(name = "Requirements",user = BaseHandler.user(self), requirements = requirements, project_id = project_id))

    def put(self, project_id):
        project = Project.query(Project.project_id == int(project_id)).get()
        parent = cgi.escape(self.request.get("parent"))
        id = int(cgi.escape(self.request.get("id")))
        description = cgi.escape(self.request.get("description"))
        title = cgi.escape(self.request.get("title"))
        method = cgi.escape(self.request.get("method"))
        if method == "update":
            requirement = Requirements.query(Requirements.req_id == id ).get()
            requirement.req_title = title
            requirement.req_desc = description
            if parent != "None":
                requirement.parent_id = parent
            requirement.put()
        else:
            requirement = Requirements(project_id=project.key, req_title=title, req_desc=description)
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

    # def update(self, requirement_id):
    #     requirement = Requirements(Requirements.key == requirement_id)
    #     parent = cgi.escape(self.request.get("parent"))
    #     description = cgi.escape(self.request.get("description"))
    #     title = cgi.escape(self.request.get("title"))
    #     requirement.parent_id = parent
    #     requirement.req_desc = description
    #     requirement.req_title = title
    #     try:
    #         requirement.put()
    #         self.response.status_int = 200
    #         self.response.status_message = "Requirement Updated Successfully"
    #     except:
    #         self.response.status_int = 500
    #         self.response.status_message = traceback.format_exception()