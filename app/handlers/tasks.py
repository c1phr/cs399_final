import os
import traceback
from google.appengine.ext import ndb
import webapp2, cgi
import json
from google.appengine.api import urlfetch
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User, Project, Requirements, Task, Project_User
from jinja2 import Environment, PackageLoader

env = Environment(loader=PackageLoader('app', 'templates'), extensions=['jinja2.ext.loopcontrols'])


class IndividualTask(BaseHandler):
    def get(self, user_key):
        template = env.get_template("tasks.html")
        try:
            tasks = Task.query(Task.assignee == user_key or self.user().key).fetch()
        except TypeError:
            tasks = Task.query(Task.assignee == self.user().key).fetch()
        self.response.write(template.render(name="Tasks", user=BaseHandler.user(self), tasks=tasks))

    def put(self):
        requirement = cgi.escape(self.request.get("requirement"))
        description = cgi.escape(self.request.get("description"))
        title = cgi.escape(self.request.get("title"))
        task_status = cgi.escape(self.request.get("open"))

        if self.request.get("task_key"):  # Update
            task = ndb.Key(urlsafe=cgi.escape(self.request.get("task_key"))).get()
        else:  # Create
            task = Task()

        task.task_title = title
        task.task_desc = description
        task.requirement = requirement or None
        task.open = task_status or True

        try:
            task.put()
            self.response.status_int = 200
            self.response.status_message = "Task Saved Successfully"
        except:
            self.response.status_int = 500
            self.response.status_message = traceback.format_exception()


class TaskDashboard(BaseHandler):
    def get(self, requirement):
        template = env.get_template("tasks.html")
        try:
            new_req = ndb.Key(urlsafe=cgi.escape(requirement)).get()
        except TypeError: # Got here but the parameter wasn't a requirement key
            self.redirect('/alltasks/' + requirement)
        tasks = Task.query(Task.requirement == new_req.key).fetch()
        for task in tasks:
            user_object = task.assignee
            current_user = User.query(User.key == user_object).get()
            task.user = current_user.user_id
            if task.open == True:
                task.mode = ""
            else:
                task.mode = "hide"

        project = Project.query(Project.key == new_req.project_id).get()
        users = Project_User.query(Project_User.project_id == project.key).fetch()
        for user in users:
            user.username = User.query(User.key == user.user_id).get().user_id
        self.response.write(template.render(name="Tasks", user=BaseHandler.user(self), tasks=tasks, project_data = project, users = users, requirement = new_req))

    def put(self, req):
        requirement = cgi.escape(self.request.get("requirement"))
        description = cgi.escape(self.request.get("description"))
        title = cgi.escape(self.request.get("title"))
        assignee = ndb.Key(urlsafe=cgi.escape(self.request.get("assignee"))).get()

        task_status = cgi.escape(self.request.get("open"))

        if self.request.get("task_key"):  # Update
            task = ndb.Key(urlsafe=cgi.escape(self.request.get("task_key"))).get()
        else:  # Create
            task = Task()

        task.task_title = title
        task.task_desc = description
        task.assignee = assignee.key
        if requirement:
            task.requirement = ndb.Key(urlsafe=requirement)
        else:
            task.requirement = None

        if task_status == "False":
            task.open = False
        else:
            task.open = True

        try:
            task.put()
            self.response.status_int = 200
            self.response.status_message = "Task Saved Successfully"
        except:
            self.response.status_int = 500
            self.response.status_message = traceback.format_exception()