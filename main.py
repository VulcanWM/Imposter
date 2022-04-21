import random
from flask import Flask, render_template, request
import os
from lists import gnames, bnames, lnames, persos, selfsus, annoysus, nerdsus, darksus, depresus, dumbsus
from functions import getcookie, delcookie, addcookie, gethashpass, makeaccount, allusers, changelose, changewin, changescore, getuser, userscorerank, userwinrank
from werkzeug.security import check_password_hash
secretkey = os.getenv("SECRET_KEY")
app = Flask(__name__)
app.config['SECRET_KEY'] = secretkey

@app.route('/')
def index():
  return render_template("index.html", danger=False, success=False, cookie=getcookie("User"))

@app.route("/game")
def game():
  if getcookie("User") == False:
    return render_template("index.html", danger="You have to login to play!", success=False, cookie=getcookie("User"))
  user = getcookie("User")
  delcookie("hi")
  addcookie("User", user)
  people = []
  lines = []
  for i in range(4):
    genders = "male", "female"
    gender = random.choice(genders)
    person = {}
    person['Gender'] = gender
    if gender == "male":
      name = random.choice(bnames) + " " + random.choice(lnames)
      person['Name'] = name
    if gender == "female":
      name = random.choice(gnames) + " " + random.choice(lnames)
      person['Name'] = name
    perso = random.choice(persos)
    person['Personality'] = perso
    people.append(person)
  imposter = random.choice(people)
  for person in people:
    suslist = {"annoying": annoysus, "self obsessed": selfsus, "nerd": nerdsus, "dark": darksus, "depressed": depresus, "dumb": dumbsus}
    if imposter == person:
      somelist = suslist
      del suslist[person['Personality']]
      allkeys = []
      for key in somelist:
        allkeys.append(key)
      theperso = random.choice(allkeys)
      lines.append(person['Name'] + "(" + person['Personality']  + " person): " + random.choice(somelist[theperso]) + "\n")
    else:
      lines.append(person['Name'] + "(" + person['Personality']  + " person): " + random.choice(suslist[person['Personality']]) + "\n")
  addcookie("Imposter", imposter['Name'])
  return render_template("game.html", lines=lines, people=people)

@app.route("/guess/<name>")
def guess(name):
  if getcookie("Imposter") == False:
    return "<h1><a href='/'>Home</a></h1><title>Imposter</title><div class='text'>You haven't started the game yet!<br><a href='/game'>Click here</a> to play!</div><style>body {background-color: #2a2727;}.text {color: white; font-size: 20px;}a{color: rgba(25, 69, 165, 0.932)}a:hover{color: #0099ff}</style>"
  if str(getcookie("Imposter")).lower() == name.lower():
    user = getcookie("User")
    delcookie("hi")
    addcookie("User", user)
    changewin(user, 1)
    changescore(user, 1)
    return "<h1><a href='/'>Home</a></h1><title>Imposter</title><div class='text'>You are right!<br><a href='/game'>Click here</a> to play again!</div><style>body {background-color: #2a2727;}.text {color: white; font-size: 20px;}a{color: rgba(25, 69, 165, 0.932)}a:hover{color: #0099ff}</style>"
  else:
    user = getcookie("User")
    delcookie("hi")
    addcookie("User", user)
    changelose(user, 1)
    changescore(user, -1)
    return "<h1><a href='/'>Home</a></h1><title>Imposter</title><div class='text'>Wrong!<br><a href='/game'>Click here</a> to play again!</div><style>body {background-color: #2a2727;}.text {color: white; font-size: 20px;}a{color: #0099ff}a:hover{color: rgba(45, 75, 141, 0.932)}</style>"

@app.route("/login")
def logint():
  if getcookie("User") == False:
    return render_template("login.html", danger=False, success=False, cookie=getcookie("User"))
  else:
    return render_template("index.html", danger="You are already logged in!", success=False)

@app.route("/signup")
def signupt():
  if getcookie("User") == False:
    return render_template("signup.html", danger=False, success=False)
  else:
    return render_template("index.html", danger="You are already logged in!", success=False, cookie=getcookie("User"))

@app.route("/login", methods=['POST', 'GET'])
def login():
  if request.method == "POST":
    username = request.form['username']
    if gethashpass(username) == False:
      return render_template("login.html", danger="This is not a real username!", success=False)
    password = request.form['password']
    if check_password_hash(gethashpass(username), password) == False:
      return render_template("login.html", danger="Wrong password!", success=False)
    addcookie("User", username)
    return render_template("index.html", danger=False, success="Login Successful!", cookie=getcookie("User"))

@app.route("/signup", methods=['POST', 'GET'])
def signup():
  if request.method == "POST":
    username = request.form['username']
    if username.lower() in allusers():
      return render_template("signup.html", danger="A user has this username! Try another one!", success=False)
    password = request.form['password']
    passworda = request.form['passwordagain']
    if password != passworda:
      return render_template("signup.html", danger="The two passwords don't match!", success=False)
    makeaccount(username, password)
    addcookie("User", username)
    return render_template("index.html", danger=False, success="Account made!", cookie=getcookie("User"))

@app.route("/logout")
def logout():
  if getcookie("User") == False:
    return render_template("index.html", danger="You have not logged in!", success=False, cookie=getcookie("User"))
  delcookie("User")
  return render_template("index.html", danger=False, success="Logout Successful!", cookie=getcookie("User"))

@app.route("/profile")
def profile():
  if getcookie("User") == False:
    return render_template("index.html", danger="You have not logged in!", success=False, cookie=getcookie("User"))
  user = getuser(getcookie("User"))
  scorerank = str(userscorerank(getcookie("User")))
  if int(scorerank) % 10 == 1 and int(scorerank) != 11:
    scorerank = scorerank + "st"
  elif int(scorerank) % 10 == 2 and int(scorerank) != 12:
    scorerank = scorerank + "nd"
  elif int(scorerank) % 10 == 3 and int(scorerank) != 13:
    scorerank = scorerank + "rd"
  else:
    scorerank = scorerank + "st"
  winrank = str(userwinrank(getcookie("User")))
  if int(winrank) % 10 == 1 and int(winrank) != 11:
    winrank = winrank + "st"
  elif int(winrank) % 10 == 2 and int(winrank) != 12:
    winrank = winrank + "nd"
  elif int(winrank) % 10 == 3 and int(winrank) != 13:
    winrank = winrank + "rd"
  else:
    winrank = winrank + "st"
  user['Scorerank'] = scorerank
  user['Winrank'] = winrank
  return render_template("profile.html", success=False, danger=False, user=user)

app.run(host='0.0.0.0', port=8080)