# this file is similar to postController.js
import models

# a blueprint is a way to create a self-contained grouping
# of related functionalities in an app
# we will use Blueprints to create basically a container
from flask import Blueprint

# BLUEPRINT

# creating our blueprint
# first arug is the blueprints name
# secong arg is its import_name
# similar to creating a router in express
posts = Blueprint('posts', 'posts')



# POST INDEX ROUTE
@posts.route('/', methods=['GET'])
def posts_index():
  return "posts resource working"

# POST CREATE ROUTE
# note: for this route you need a trailing slash (i.e. /)
@posts.route('/', methods=['POST'])
def create_dog():
  return "you hit dog create route"
