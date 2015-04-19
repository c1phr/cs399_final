import webapp2
from webapp2_extras import sessions
from app.models.models import User


'''
BaseHandler class to expose session
Session GET: self.session.get('<prop_name>') -> Then dump this to the template
Session INSERT: self.session['<prop_name>'] = <value>
'''
class BaseHandler(webapp2.RequestHandler):
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

    def rest_req(func):
        """ Decorator to handle spoofing RESTful verbs """
        def inner(handler):
            params = handler.request.params
            if 'http_verb' in params:
                if params['http_verb'] == 'PUT':
                    handler.put()
                elif params['http_verb'] == 'DELETE':
                    handler.delete()
        return inner