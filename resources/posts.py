# this file is similar to postController.js
import models

# a blueprint is a way to create a self-contained grouping
# of related functionalities in an app
# we will use Blueprints to create basically a container
from flask import Blueprint, request, jsonify
# request - data from client's request is send to the global request object
# we can use this object to get the json or form data or whatever is in the request
# the request global var will be reassigned every time a request comes in that
# has a body (POST, PUT)

# this is some useful tools that come with peewee
from playhouse.shortcuts import model_to_dict



# BLUEPRINT

# creating our blueprint
# first arug is the blueprints name
# secong arg is its import_name
# similar to creating a router in express
posts = Blueprint('posts', 'posts')



# POST INDEX ROUTE
@posts.route('/', methods=['GET'])
def posts_index():
  results = models.Post.select()

  print('result of dog select query')
  print(result)

  for row in result:
    print(row)

  post_dicts = [model_to_dict(post) for post in result]

  print(post_dicts)

  return jsonify({
    'data': post_dicts,
    'message': f"Successfully found {len(post_dicts)} dogs",
    'status': 200
  }), 200







# POST CREATE ROUTE
# note: for this route you need a trailing slash (i.e. /)
@posts.route('/', methods=['POST'])
def create_post():
  # .get_json() attache to request will extract JSON from req.body
  payload= request.get_json() # this is like req.body in express!!!
  print(payload) # you should see request body in your terminal
  new_post = models.Post.create(description=payload['description'], user=payload['user'], comment=payload['comment'])

  print(new_post) # just prints the ID -- check sqlite3 to see the data
                  # run sqlite3 dogs.sqlite and run SQL queries in the CLI

  # we can use model_to_dict from playhouse
  post_dict = model_to_dict(new_post)

  return jsonify(
    data=dog_dict,
    message="Successfully created post!",
    status=201
  ), 201
