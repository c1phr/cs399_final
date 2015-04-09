import os
import webapp2
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('app', 'templates'))
class MainHandler(webapp2.RequestHandler):
    def get(self):
        template = env.get_template('index.html')
        self.response.write(template.render())