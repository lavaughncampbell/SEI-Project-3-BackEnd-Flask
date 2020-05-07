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

from flask_login import current_user, login_required

# <-------------------------------------->

# BLUEPRINT

# creating our blueprint
# first arug is the blueprints name
# secong arg is its import_name
# similar to creating a router in express
posts = Blueprint('posts', 'posts')






# <-------------------------------------->
# POST INDEX ROUTE
@posts.route('/', methods=['GET'])
@login_required
def posts_index():

  current_user_post_dicts = [model_to_dict(post) for post in current_user.posts]

  for post_dict in current_user_post_dicts:
    post_dict['user'].pop('password')

  print(current_user_post_dicts)

  return jsonify({
    'data': current_user_post_dicts, 
    'message': f"Successfully found {len(current_user_post_dicts)} posts",
    'status': 200
  }), 200












# <-------------------------------------->
# POST CREATE ROUTE
# note: for this route you need a trailing slash (i.e. /)
@posts.route('/', methods=['POST'])
@login_required # you should have to be logged in to add a post 
def create_post():
  # .get_json() attache to request will extract JSON from req.body
  payload= request.get_json() # this is like req.body in express!!!
  print(payload) # you should see request body in your terminal

  new_post = models.Post.create(
    description=payload['description'], 
    user=current_user.id, # using the logged in user to set this 
    comment=payload['comment']
  )

  print(new_post) # just prints the ID -- check sqlite3 to see the data
                  # run sqlite3 dogs.sqlite and run SQL queries in the CLI

  # we can use model_to_dict from playhouse
  post_dict = model_to_dict(new_post)

  print(post_dict) # check it out! the user should be attached 

  post_dict['user'].pop('password') # remove password from user 

  return jsonify(
    data=post_dict,
    message="Successfully created post!",
    status=201
  ), 201







# <-------------------------------------->
# POST DELETE ROUTE 
@posts.route('/<id>', methods=['DELETE'])
@login_required # you should be logged in to delete 
def delete_post(id):
  try:
    # get a post 
    post_to_delete = models.Post.get_by_id(id)

    # see if the user matches 

    # if so 
    if post_to_delete.user.id == current_user.id:

      #delete it 
      post_to_delete.delete_instance() 


      return jsonify(
        data={}, 
        message=f"Successfully deleted post with id {id}", 
        status=200
      ), 200

    else: # post doesn't below to the user

      return jsonify(
        data={
        'error': '403 Forbidden'
        }, 
        message="Post user id does not match posts id. User can only delete their own posts.", 
        status=403
      ), 403

  except models.DoesNotExist:
    return jsonify(
      data={
        'error': '404 Not found'
      }, 
      message="There is no post with that ID.", 
      status=404
      ), 404




# <-------------------------------------->
# POST UPDATE ROUTE 
@posts.route('/<id>', methods=['PUT'])
@login_required # you got no business changing data if your not logged in
def update_post(id):
  payload = request.get_json()

  # get the post 
  post_to_update = models.Post.get_by_id(id)
  print("HERE IS UPDATED HERE")
  print(post_to_update)
  print("THIS IS THE POST description")
  print(post_to_update.description)
  print('HERE IS PAYLOAD!')
  print(payload)
  # see if the post belongs to the logged in user 
  if post_to_update.user.id == current_user.id:
    # if 'description' in payload:
    post_to_update.description = payload['description']
    # if 'comment' in payload: 
    post_to_update.comment = payload['comment']

    # post_to_update.save() # this is nice, ORMs are great 

    updated_post_dict = model_to_dict(post_to_update)

    updated_post_dict['user'].pop('password') 

    return jsonify(
      data=updated_post_dict, 
      message=f"Successfully updated post with id {id}", 
      status=200
    ), 200 

  else:
    return jsonify(
      data={
        'error': '403 Forbidden'
      }, 
      message="Post user's id does not match post id, User can only update their own posts.", 
      status=403
      ), 403



# <-------------------------------------->
# POST SHOW ROUTE 
@posts.route('/<id>', methods=['GET'])
def show_post(id):
  post = models.Post.get_by_id(id)

  post_dict = model_to_dict(post)


  # if user not logged in, the can only see description and commend 
  if not current_user.is_authenticated:
    return jsonify(
      data={
        'description': post.description, 
        'comment': post.comment
      }, 
      message="Registered users can see more info about this post", 
      status=200
    ), 200

  else:
    return jsonify({
    'data': post_dict, 
    'message': f"Successfully found posts",
    'status': 200
  }), 200






