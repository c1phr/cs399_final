import os
import webapp2
from app.handlers.BaseHandler import BaseHandler
from app.models.models import User
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))

