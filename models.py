# all of our models will go in this file
# our entire database setup will be in this file

#peewee in our flaskapp is like mongoose in our express app
from peewee import *
import datetime # built in to python
                # in python you often need to
                # already be there in other languages
                # this keeps it lightweight


# import * means import everything..
# Sqlite Database -- adapter that lets us connect to sqlite databases

# and
# Model -- this Model() class is what we will inherit from when
# defining our models (similar to what we did in mongoose in unit 2)
# use peewee to create our MODELS!!!!!
# Peewee docs are a great resource when setting up our app.

# we will use the flask_login module to set up our user model, sessions
# logins, authentication, requiring authentication for certain things
# our User class (model) will inherit from this UserMixin
from flask_login import UserMixin








# What is Sqlite?

# sqlite lets you store your entire database in just a file
# so its a really good tool for developement
# all your data in one file
# great for development bc you can have easily portable database
# you can restore data really easily with sqlite
# standard way to setup databases
# postgres, mysql, microsoft sql
# database server we connected to it we ran commands to the database server on our machine
# avoid the need to setup a database server to get your app running
# when we deploy the app to a postgres database.
DATABASE = SqliteDatabase('project3DB.sqlite') # you can name it what you want
# similar to MONGO_DB_URL = mongodb://localhost/dogs, {...} in unit 2
# there will be a file in our project called dogs.sqlite // mine will be project3DB.sqlite


# define our Dog model

class Post(Model): # Post will inherit a model. Similar to model schema in express.
# in express we gave a name of each field and a data type
  description = CharField() # string
  user = CharField() # string for now, let we will implement a relation
  comment = CharField() # string
  # this is how you specify default values
  created_at: DateTimeField(default=datetime.datetime.now) #stake datetime has to be imported at top

  # inside the dog mdoel special constructor that gives our model/class instructions on
  # how to connect to a DB & where to store its data
  # specify this when you define a model.
  class Meta:
    database = DATABASE


# our User class (model) will inherit from this UserMixin
# to behave correctly in flask_login's session/login/etc functionality,
# The User class must have certain methods and properties that a standard
# Peewee model (like Dog, e.g.) doesn't have
class User(UserMixin, Model): # all models must inherit from models
  username = CharField(unique=True)
  email = CharField(unique=True)
  password = CharField()
  name = CharField()
  bootcamp = CharField()
  position = CharField()

  class Meta:
    database = DATABASE

# define a method that will get called when the app starts
# (in app.py) to set up our database connection
# similar to how we did ('./db/db.js') in server.js in unit 2
def intialize(): # NOTE we are making this name up
  DATABASE.connect() # similar to mongoose.connect(....)

  # we need to explicitly create the tables based on the schema
  # when our applications start
  # definitions above
  # use .create_tables()
  # first arg: is a LIST of table to create
  # second arg --safe=True -- only create tables if they don't already exists.
  DATABASE.create_tables([User, Post], safe=True) # this is create a Post list here
  print("Connected to DB and created tables if they weren't already there")


  # after everytime we interact with the sql database we need to close the connection
  # with SQL, DONT leave DB connection open, we don't want to
  # god up space in the connection pool
  DATABASE.close()




