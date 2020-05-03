# this is like your server.js in express it holds all the important info
from flask import Flask, jsonify # similar to const express = require('express')
# we're now also importing jsonify from flask
# jsonify let's us send JSON HTTP responses (like res.json)



from resources.posts import posts # import blueprint from resources.posts
                                  # think "const dogController = require('./controllers/dogController.js')
from resources.users import users # import blueprint from
# resources.users

# in python when you import a file, you get everything in the "global scope"
# this import models will import everything.
# so this statement will import all variables and methods/function from that
# file as properties on the models object. (e.g.models.intialize() will be
# available in this file, etc)...note that we did notexplicitly "export"
# anything in models.py
# google out "namespacing in python and importing"
import models # so everything is ready when we start our app.

from flask_cors import CORS # importing CORS here

# we need to import and configure the login manager
# the login manager is the main tool for coordinating sessions and login stuff in our app.
from flask_login import LoginManager

DEBUG=True # this will print nice helpful errors messages since we are developing
PORT=8000

# this is similar to const app = express()
app = Flask(__name__) # instantiating the Flask class to create an app



# CORS - Cross Origin Resource Sharing 
# a web domain (site/port/etc) is an "origin"
# this app is localhost: 8000 that's an "origin"
# our react app is localhost:3000 that's an origin 
# Browsers implement CORS to prevent a JS app from sending requests 
# Configuring CORS lets server say "heres' whatr im expecting to hear from"



# configuring the LoginManager, according to this:
# we need to do several things
# 1. setup a secret/key for sessions
app.secret_key = "Making. Sommething Very. This is a huge secret."

# 2. instantiate the LoginManager to actually get a login_manager
login_manager = LoginManager()

# 3. actually connect the app with the login manager. Doing this b/c docs says so.
login_manager.init_app(app)


# in reg and login, we did login_user(user that was found or created)
# doing that stored the ID of that user in the session
# but in our routes we want to work with the user object
# so we need to set it up so that the user object is landed
# when user is logged in


# <-------------------------------------->
# LOGIN MANAGER 

@login_manager.user_loader # this allows us to access our User Object
def load_user(user_id):
  try:
    print("loading the following user")
    user = models.User.get_by_id(user_id) # IMPORTANT CHANGE
                                          # USE GET_BY_ID
                                          # Docs seem wrong

    return models.User.get(user_id)
  except models.DoesNotExist:
    return None


@login_manager.unauthorized_handler
def unauthorized():
  return jsonify(
    data={
      'error': 'User not logged in'
    }, 
    message="You must be logged in to access that resource", 
    status=401
  ), 401




# <-------------------------------------->
# CORS -- Cross Origin Resource Sharing 

CORS(users, origins=['http://localhost:3000'],
  supports_credentials=True)
CORS(posts, origins=['http://localhost:3000'],
  supports_credentials=True)




# <-------------------------------------->
# BLUEPRINTS (Controller of the app)

app.register_blueprint(posts, url_prefix='/api/v1/posts')
app.register_blueprint(users, url_prefix='/api/v1/users')







# <-------------------------------------->
# TEST ROUTES 

#here is how you write a route in Flask
@app.route('/') # @ symbol here means this is decorator
def hello():
  # what gets returned from a route is what is sent back as response
  return 'Hello, world!'

#flask is little finicky

def get_list():
  return ['hello', 'hi', 'hey']

@app.route('/test_json')
def get_json():
    # here we are using jsonify to create an HTTP Response
    # with Content-Type set to json
    # similar to res.json() in express
    return jsonify(['hello', 'hi', 'hey'])

@app.route('/cat_json')
def get_cat_json():
  # you can pass key value pairs into jsonify()
  return jsonify(name="Nico", age=15)

# you can use a dictionary as the value of a key-value pair in jsonify()
@app.route('/nested_json')
def get_nested_json():
  nico = {
  'name': 'Nico',
  'age': 15,
  'handsome': True,
  'sweet': True
  }
  return jsonify(name="Reuben", age=41, cat=nico)


# can you pass an array of dicts
@app.route('/two_cats')
def get_two_cats():
  nico = {
  'name': 'Nico',
  'age': 15,
  'handsome': True,
  'sweet': True
  },
  rocky = {
  'name': 'Rocky',
  'age': 7,
  'handsome': True,
  'sweet': True
  }
  return jsonify(name="Reuben", age=41, cat=[nico, rocky])


# can you send back just a dictionary? let's see
@app.route('/dict_as_json')
def get_dict_as_json():
  return jsonify({
    'city_name': 'Chicago',
    'population': 3000000,
    'mayor': 'Lightfoot',
    'neighborhoods': [{
      'name': 'Rodgers Park',
      'zip': 60626,
    }, {
      'name': 'Edgewater',
      'zip': 60626
    }, {
      'name': 'Albany Park',
      'zip': 60626
    }]
    })

# URL Parameters in Flask
# like (req.params in express: app.get('/hello/:name'))
# ':name' would be the URL parameter. Value will be specified in the future.
@app.route('/say_hello/<username>')
def say_hello(username): # this func take the URL param as an argument
  return "Hello {}".format(username)




# <-------------------------------------->
# LISTENER  

# this is similar to app.listen() in express
# it goes at the bottom. __name__ being '__main___'
# means we just ran this file from the command line
# as opposted to exporting it.
if __name__ == '__main__':
  # when we start the app, set up our DB/tables as defined in models.py
  models.intialize() # remember in express we required db before we did app.listen
  app.run(debug=DEBUG, port=PORT)


# When building a API with the python framework flask
# we don't need the front end we are backend web deveelopers!

# We are just focusing on API's building end points that return JSON!!!
# Ex. you want data about cats cool ill give you some JSON about cats.
# How you display that info on the screen is up to you! I am a backend developer
# I DONT CARE I can set up your database for you and your server ill give you the data.

# CLOSE THE BROWSER AND START USING POSTMAN
# WE ARE GOING TO USE POSTMAN TO MAKE OUR REQUESTS
# POSTMAN Allows you to simulate a front end without
# having to build one!!!!!!IMPORTANT!!
# The front end basically from the standpoint of the server
# the front end is just asking you for data all the time.
# It's going to be POST data, it's going to be GET data,
# PUT data, DELETE data. #So you don't have to worry about whats happening
# with react when your building your backend you just know if someone asks for
# data im going to give it back to them.


# no more browser just postman back end development gets rid of those templates
# postman will pretend to be a browser
# front end just needs to know the type of requests and the urls
# use postman to access your endpoints



#NOW LETS MAKE A DOG APP

# WHEN BUILDING A SERVER YOU MUST HAVE YOUR MODELS SORTED OUT FIRST!!!
# IF WE ARE GOING TO STORE MODELS WE NEED TO CONFIGURE OUR APP TO USE
# A DATABASE

# WERE GOING TO INSTALL ACOUPLE MODULES

# pip3 install peewee psycopg2

# psycopg2 -- lets our app connect to a database

# peewee -- ORM
#   ORM -- Object Relational Mapping
#   -- LIKE AN orm
#   -- allows us to create models
#   -- allows us to query our DB in our flask app.

#   !! REMEMBER TO pip3 freeze > requirements.txt manually!!!!
#   -- pip (pip3) will do this for you

#   if you need to clone a flask app and get it set up and
#   install everything in requirements.txt
#   in a new directory


