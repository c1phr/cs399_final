import os
import webapp2
from google.appengine.ext import ndb

class UserInformation(ndb.Model):
    first_name = ndb.StringProperty()
    last_name = ndb.StringProperty()
    email = ndb.StringProperty()