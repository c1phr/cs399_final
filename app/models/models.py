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
    req_id = ndb.IntegerProperty(required=True)
    parent_id = ndb.KeyProperty(kind="Requirements")
    req_desc = ndb.TextProperty()
    project_id = ndb.KeyProperty(kind="Project")

class Project(ndb.Model):
    project_id = ndb.IntegerProperty(required=True)
    project_title = ndb.StringProperty()
    project_desc = ndb.TextProperty()
    project_owner = ndb.KeyProperty(kind="User")

class Task(ndb.Model):
    task_id = ndb.IntegerProperty(required=True)
    task_title = ndb.StringProperty()
    req_id = ndb.KeyProperty(kind="Requirements")
    assignee_id = ndb.KeyProperty(kind="User")
    field = ndb.StringProperty()

class Project_User(ndb.Model):
    project_id = ndb.KeyProperty(kind="Project")
    user_id = ndb.KeyProperty(kind="User")