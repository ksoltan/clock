from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
import logging

class UserPrefs(ndb.Model):
    tz_offset = ndb.FloatProperty(default = 0)
    user = ndb.UserProperty(auto_current_user_add = True)

    def cache_set(self):
        logging.info('cache set')
        memcache.set('UserPrefs:' + self.key.string_id(), self)

    def put(self):
        super(UserPrefs, self).put()
        self.cache_set()

def get_userprefs(user_id = None):
    if not user_id:
        user = users.get_current_user()
        if not user:
            return None
        user_id = user.user_id()

    userprefs = memcache.get('UserPrefs:' + user_id)
    if not userprefs:
        key = ndb.Key('UserPrefs', user_id)
        userprefs = key.get()
        if userprefs:
            userprefs.cache_set()
        else:
            userprefs = UserPrefs(id = user_id)
    return userprefs
