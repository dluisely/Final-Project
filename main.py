"""Simple example app to demonstrate storing info for users.

CSSI-ers!  If you want to have users log in to your site and store
info about them, here is a simple AppEngine app demonstrating
how to do that.  The typical usage is:

- First, user visits the site, and sees a message to log in.
- The user follows the link to the Google login page, and logs in.
- The user is redirected back to your app's signup page to sign
  up.
- The user then gets a page thanking them for signup.

- In the future, whenever the user is logged in, they'll see a 
  message greeting them by name.

Try logging out and logging back in with a fake email address
to create a different account (when you "log in" running your
local server, it doesn't ask for a password, and you can make
up whatever email you like).

The key piece that makes all of this work is tying the datastore
entity to the AppEngine user id, by passing the special property
id when creating the datastore entity.

cssi_user = CssiUser(..., id=user.user_id())
cssi_user.put()

and then, looking it up later by doing

cssi_user = CssiUser.get_by_id(user.user_id())
"""

import webapp2

from google.appengine.api import users
from google.appengine.api import images
from google.appengine.ext import ndb

class CssiUser(ndb.Model):
  """CssiUser stores information about a logged-in user.

  The AppEngine users api stores just a couple of pieces of
  info about logged-in users: a unique id and their email address.

  If you want to store more info (e.g. their real name, high score,
  preferences, etc, you need to create a Datastore model like this
  example).  
  """
  first_name = ndb.StringProperty()
  last_name = ndb.StringProperty()
  
  product_name = ndb.StringProperty()
  product_description = ndb.StringProperty()
  product_picture = ndb.BlobProperty()
  trade_request = ndb.StringProperty()

class MainHandler(webapp2.RequestHandler):
  def get(self):
    user = users.get_current_user()
    # If the user is logged in...
    if user:
      email_address = user.nickname()
      cssi_user = CssiUser.get_by_id(user.user_id())
      signout_link_html = '<a href="%s">sign out</a>' % (
          users.create_logout_url('/'))
      # If the user has previously been to our site, we greet them!
      if cssi_user:
        self.response.write('''
            Welcome %s %s (%s)! <br> %s <br>''' % (
              cssi_user.first_name,
              cssi_user.last_name,
              email_address,
              signout_link_html))
      # If the user hasn't been to our site, we ask them to sign up
      else:
        self.response.write('''
            Welcome to our site, %s!  Please sign up! <br>
            <form method="post" action="/">
            <label> Product Name </label>
            <input type="text" name="product_name">
            <label> Description </label>
            <input type="text" name="product_description">
            <label> Trade Request </label>
            <input type="text" name="trade_request">
            <input type="submit">
            </form><br> %s <br>
            ''' % (email_address, signout_link_html))
    # Otherwise, the user isn't logged in!
    else:
      self.response.write('''
        Please log in to use our site! <br>
        <a href="%s">Sign in</a>''' % (
          users.create_login_url('/')))

  def post(self):
    user = users.get_current_user()
   
    if not user:
      # You shouldn't be able to get here without being logged in
      self.error(500)
      return
    cssi_user = CssiUser(
        product_name=self.request.get('product_name'),
        product_description=self.request.get('product_description'),
        trade_request=self.request.get('trade_request'),
        id=user.user_id())
    cssi_user.put()
    self.response.write('Thanks for signing up, %s!' % 
        cssi_user.first_name)

app = webapp2.WSGIApplication([
  ('/', MainHandler)
], debug=True)
