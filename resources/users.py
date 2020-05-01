# this is like a user controller
# or auth controller

import models # get all the models. specifically user model

from flask import Blueprint # Blueprint is how we make our controllers

# make this a blueprint
users = Blueprint('users', 'users')

@users.route('/', methods=['GET'])
def test_user_resource():
  return "user resource works"
