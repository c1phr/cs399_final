from app.handlers.BaseHandler import BaseHandler
import cgi, urllib, json
from app.models.models import User

from google.appengine.api import urlfetch
from secrets import secrets


class Login(BaseHandler):
    def get(self):
        if not self.request.get('code'):
            url = 'https://github.com/login/oauth/authorize?client_id=' + secrets.GitHub_ClientID() + "&scope=user,repo,notifications,gist,read:repo_hook, write:repo_hook"
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

        info_url = "https://api.github.com/user?access_token=" + auth_contents["access_token"]
        username_result = urlfetch.fetch(url = info_url,
                                method=urlfetch.GET,
                                headers={"Accept": "application/json"},
                                deadline=10)
        user_contents = json.loads(username_result.content)

        user = User.query(User.user_id == user_contents["login"]).get()
        if user == None:
            self.session["username"] = user_contents["login"]
            self.session["gravatar"] = user_contents["avatar_url"]
            self.redirect("/register")
        else:
            self.redirect("/")