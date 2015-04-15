from app.handlers.BaseHandler import BaseHandler
import cgi, urllib, json
from github import Github, GithubException
from google.appengine.api import urlfetch
from lib.secrets import secrets


class Login(BaseHandler):
    def get(self):
        if not self.request.get('code'):
            url = 'https://github.com/login/oauth/authorize?client_id=' + secrets.GitHub_ClientID()
            return self.redirect(url)
        code = cgi.escape(self.request.get('code'))
        access_url = "https://github.com/login/oauth/access_token"
        data_vals = {"client_id": secrets.GitHub_ClientID(),
                     "client_secret": secrets.GitHub_ClientSecret(),
                     "code": code}
        data = urllib.urlencode(data_vals)
        result = urlfetch.fetch(url = access_url,
                                payload=data,
                                method=urlfetch.POST,
                                headers={"Accept": "application/json"},
                                deadline=10)
        auth_contents = json.loads(result.content)
        self.session["access_token"] = auth_contents["access_token"]
        self.session["access_token_type"] = auth_contents["token_type"]
        self.session["access_token_scope"] = auth_contents["scope"]
        self.redirect("/")




class TwoFactor(BaseHandler):
    def get(self):
        # Show the user the two factor form
        pass