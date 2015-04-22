import webapp2
from webapp2_extras import sessions
from app.fakextures import Fakextures
from app.models.models import User


'''
BaseHandler class to expose session
Session GET: self.session.get('<prop_name>') -> Then dump this to the template
Session INSERT: self.session['<prop_name>'] = <value>
'''
class BaseHandler(webapp2.RequestHandler):
    def __init__(self, request, response):
        self.initialize(request, response)
        Fakextures.install_fixtures()

    def dispatch(self):
        self.session_store = sessions.get_store(request=self.request)

        try:
            webapp2.RequestHandler.dispatch(self)
        finally:
            self.session_store.save_sessions(self.response)

    @webapp2.cached_property
    def session(self):
        return self.session_store.get_session(backend='memcache')

    '''
    Gets a user object based on the user key passed in.
    Returns None if user doesn't exist
    '''
    def get_user(self, user_key):
        if not user_key or user_key == "":
            raise Exception("Invalid User_Key")
        user = User.query(User.key == user_key)
        return user

    #Returns user's username
    def user_id(self):
        user = User.query(User.key == self.session.get("user")).get()
        return user.user_id

    #Returns user email
    def user_email(self):
        user = User.query(User.key == self.session.get("user")).get()
        return user.email

    #Returns user first name
    def user_first(self):
        user = User.query(User.key == self.session.get("user")).get()
        return user.first

    #Returns user last name
    def user_last(self):
        user = User.query(User.key == self.session.get("user")).get()
        return user.last

    #Returns user gravatar
    def user_gravatar(self):
        user = User.query(User.key == self.session.get("user")).get()
        return user.gravatar_url

    #Returns entire user object
    def user(self):
        user = User.query(User.key == self.session.get("user")).get()
        return user
