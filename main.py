#!/usr/bin/env python
import os
import jinja2
import webapp2
from guest import Guest


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")
    
    

class GuestHandler(BaseHandler):
    def get(self):
        return self.render_template("guestbook.html")

    def post(self):
        ime = self.request.get("ime")
        priimek = self.request.get("priimek")
        email = self.request.get("email")
        sporocilo = self.request.get("sporocilo")

        if not ime:
            ime = "Neznanec"

        if not "<script>" in sporocilo:

            guest = Guest(ime=ime, priimek=priimek, email=email, sporocilo = sporocilo)
            guest.put()
            return self.redirect_to("main")
        
        else:
            sprocilo = ""
            return self.redirect_to("main")
    

class AllMessagesHandler(BaseHandler):
    def get(self):

        seznam = Guest.query().fetch()
        params = {"seznam":seznam}
        
        return self.render_template("seznam-sporocil.html", params = params)

    

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler, name="main"),
    webapp2.Route('/all-messages', AllMessagesHandler),
    webapp2.Route('/new-guest', GuestHandler),
], debug=True)
