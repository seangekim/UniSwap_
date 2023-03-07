import pymongo
from pymongo import MongoClient

from flask import Flask, jsonify, request, session, redirect
# from passlib.hash import pbkdf2_sha256
# from app import db
import uuid

cluster = MongoClient("mongodb+srv://cjdewitt:d8ZpfzggeDVYvHMO@uni-swap.hy9bzs8.mongodb.net/?retryWrites=true&w=majority")
db = cluster["uni-swap"]
collection = db["users"]

class User:

  # Assigns parameters to an instance of a uer object
  def __init__(self, name_param, email_param, password_param):
    self.name = name_param
    self.email = email_param
    self.password = password_param


  #f
  def start_session(self, user):
    del user['password']
    session['logged_in'] = True
    session['user'] = user
    return jsonify(user), 200

  #f
  def signup(self):
    print(request.form)

    # Create the user object
    user = {
      "name": request.form.get('name'),
      "email": request.form.get('email'),
      "password": request.form.get('password')
    }

    # Encrypt the password
    # user['password'] = pbkdf2_sha256.encrypt(user['password'])

    # Check for existing email address
    if collection.find_one({ "email": 'email'}):
      return jsonify({ "error": "Signup failed! Email address already in use" }), 400

    # Check to make sure email is USC email
    elif not collection.find_one({"email" : { "$regex": "@usc.edu"}}): 
      return jsonify({ "error": "Signup failed! Email is not a USC email" }), 400

  # Insert the user
    else:
      collection.insert_one(user)
      return self.start_session(user)

  #f
  def signout(self):
    session.clear()
    return redirect('/')
  
  def loginEmail(self):

    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')

    # If user exists in db, log them in
    if collection.find_one({"name": name}, {"email": email}, {"password": password}):
      user = {
        "name" : name,
        "email" : email,
        "password" : password
      }
      User(name, email, password)
      return self.start_session(user)

    # If user does not exist in db, return error
    else:
      return jsonify({ "error": "Invalid login credentials" }), 401  


  #f
  def loginGoogle(self):
    authorization