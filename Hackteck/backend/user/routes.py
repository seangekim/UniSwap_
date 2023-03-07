from flask import Flask
import app
from models import User
from flask import request, jsonify, session, redirect



@app.routes('/user/signup', methods=['POST'])
def signup():
  return User().signup()

@app.routes('/user/signout')
def signout():
  return User().signout()

@app.routes('/user/login', methods=['POST'])
def login():
  return User().login()

@app.routes('/products', methods=['GET', 'POST'])
def product_handler():
  if request.method == 'GET':
    # Handle GET request to retrieve products
        return 'Retrieving products...'
  elif request.method == 'POST':
      # Handle POST request to create a new product
      return 'Creating a new product...'



if __name__ == '__main__':
    app.run(port=3000)