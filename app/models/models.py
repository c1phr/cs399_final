import os
import webapp2
from google.appengine.ext import ndb

class User(ndb.Model):
    user_id = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    email = ndb.StringProperty(required=True)
    gravatar_url = ndb.StringProperty()

class Requirements(ndb.Model):
    parent_id = ndb.KeyProperty(kind="Requirements", required=False)
    req_title = ndb.TextProperty()
    req_desc = ndb.TextProperty()
    project_id = ndb.KeyProperty(kind="Project")

class Project(ndb.Model):
    project_id = ndb.IntegerProperty(required=True)
    project_title = ndb.StringProperty()
    project_desc = ndb.TextProperty()
    project_owner = ndb.KeyProperty(kind="User")

class Task(ndb.Model):
    task_title = ndb.StringProperty()
    requirement = ndb.KeyProperty(kind="Requirements", required=False)
    task_desc = ndb.StringProperty()
    assignee = ndb.KeyProperty(kind="User", required=True)
    created = ndb.DateTimeProperty(auto_now_add=True)
    open = ndb.BooleanProperty(default=True)

class Project_User(ndb.Model):
    project_id = ndb.KeyProperty(kind="Project")
    user_id = ndb.KeyProperty(kind="User")
    is_owner = ndb.BooleanProperty(default=False)