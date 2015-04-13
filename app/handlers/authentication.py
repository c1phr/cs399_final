from app.handlers.BaseHandler import BaseHandler
import cgi, urllib, urllib2
from github import Github, GithubException
from secrets import secrets


class Login(BaseHandler):
    def get(self):
        if not self.request.get('code'):
            url = 'https://github.com/login/oauth/authorize?client_id=' + secrets.GitHub_ClientID()
            return self.redirect(url)
        code = cgi.escape(self.request.get('code'))
        # Do something with this code and redirect the user back home or something

    def post(self):
        if not self.session.get('username'):
            self.session['username'] = cgi.escape(self.request.get('username'))
        if not self.session.get('password'):
            self.session['password'] = cgi.escape(self.request.get('password'))
        two_factor = cgi.escape(self.request.get('two_factor'))
        gh = Github(self.session.get('username'), self.session.get('password')).get_user()
        if not two_factor:
            try:
                auth = gh.create_authorization(scopes=['repo'])
            except GithubException:
                # Redirect to a new page to get the 2FA code, then post back here with that code
                pass
        else:
            try:
                auth = gh.create_authorization(scopes=['repo'], onetime_password=two_factor)
            except GithubException:
                # Figure out how we want to display this exception
                pass




class TwoFactor(BaseHandler):
    def get(self):
        # Show the user the two factor form
        pass