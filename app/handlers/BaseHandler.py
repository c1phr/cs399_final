import webapp2
from webapp2_extras import sessions


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
        return self.session_store.get_session()