from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
import pymongo
import dns
import os
clientm = os.getenv("clientm")
mainclient = pymongo.MongoClient(clientm)
usersdb = mainclient.Profiles
profilescol = usersdb.Users

def addcookie(key, value):
  session[key] = value

def delcookie(keyname):
  session.clear()

def getcookie(key):
  try:
    if (x := session.get(key)):
      return x
    else:
      return False
  except:
    return False

def makeaccount(username, password):
  passhash = generate_password_hash(password)
  document = [{
    "Username": username,
    "Password": passhash,
    "Coins": 0,
    "Wins": 0,
    "Loses": 0,
    "Score": 0,
    "Best time": None,
    "Badges": []
  }]
  profilescol.insert_many(document)

def gethashpass(username):
  for user in profilescol.find():
    if user['Username'] == username:
      return user['Password']
  return False

def getuser(username):
  for user in profilescol.find():
    if user['Username'] == username:
      return user
  return False

def allusers():
  users = []
  for user in profilescol.find():
    users.append(user['Username'].lower())
  return users

def changewin(username, number):
  auser = getuser(username)
  user = auser
  win = user['Wins']
  del user['Wins']
  user['Wins'] = win + number
  delete = {"_id": auser['_id']}
  profilescol.delete_one(delete)
  profilescol.insert_many([user])

def changelose(username, number):
  auser = getuser(username)
  user = auser
  win = user['Loses']
  del user['Loses']
  user['Loses'] = win + number
  delete = {"_id": auser['_id']}
  profilescol.delete_one(delete)
  profilescol.insert_many([user])

def changescore(username, number):
  auser = getuser(username)
  user = auser
  win = user['Score']
  del user['Score']
  user['Score'] = win + number
  delete = {"_id": auser['_id']}
  profilescol.delete_one(delete)
  profilescol.insert_many([user])

def userscorerank(username):
  w = 0
  for auser in profilescol.find().sort("Score", -1):
    w = w + 1
    if auser['Username'] == username:
      return w

def userwinrank(username):
  w = 0
  for auser in profilescol.find().sort("Wins", -1):
    w = w + 1
    if auser['Username'] == username:
      return w