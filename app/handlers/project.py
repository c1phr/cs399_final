import os
import webapp2
from app.handlers.BaseHandler import BaseHandler
from app.models.models import UserInformation
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

