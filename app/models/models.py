import os
import webapp2
from google.appengine.ext import ndb

class User(ndb.Model):
    user_id = ndb.IntegerProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    gravatar_url = ndb.StringProperty()

class Requirements(ndb.Model):
    req_id = ndb.IntegerProperty(required=True)
    parent_id = ndb.IntegerProperty()
    req_desc = ndb.TextProperty()
    project_id = ndb.IntegerProperty()

class Project(ndb.Model):
    project_id = ndb.IntegerProperty(required=True)
    project_title = ndb.StringProperty()
    project_desc = ndb.TextProperty()

class Task(ndb.Model):
    task_id = ndb.IntegerProperty(required=True)
    task_title = ndb.StringProperty()
    req_id = ndb.IntegerProperty()
    assignee_id = ndb.IntegerProperty()
    field = ndb.StringProperty()