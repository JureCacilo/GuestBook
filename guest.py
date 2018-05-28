from google.appengine.ext import ndb

class Guest(ndb.Model):
  ime = ndb.StringProperty(default = "neznanec")
  priimek = ndb.StringProperty()
  email = ndb.StringProperty()
  sporocilo = ndb.TextProperty()
  nastanek = ndb.DateTimeProperty(auto_now_add = True)


 