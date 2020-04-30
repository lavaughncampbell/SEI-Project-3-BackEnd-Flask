# this is like your server.js in express it holds all the important info
from flask import Flask # similar to const express = require('express')


DEBUG=True # this will print nice helpful errors messages since we are developing
PORT=8000


app = Flask(__name__) # this is similar to const app = express()



#here is how you write a route in Flask
@app.route('/') # @ symbol here means this is decorator
def hello():
  return 'Hello, world!'











# this is similar to app.listen() in express
# it goes at the bottom. __name__ being '__main___'
# means we just ran this file from the command line
# as opposted to exporting it.
if __name__ == '__main__':
  app.run(debug=DEBUG, port=PORT)
