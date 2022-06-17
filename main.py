from itertools import count
from random import random
from flask import Flask, render_template, g
import sqlite3
import datetime
from collections import Counter
import requests, json



def getFullName(name):
    cur = g.db.cursor()
    toExecute = f"""SELECT DISTINCT primaryName FROM nameBasics INNER JOIN crew ON crew.p=nameBasics.nconst
WHERE crew.p = '{name}'"""
    cur.execute(toExecute)
    for row in cur:
        return row


def getBioImage(name):
    url = f"https://imdb-api.com/API/Name/k_twom815p/{name}"
    payload = {}
    headers= {}
    response = requests.request("GET", url, headers=headers, data = payload)
    jsonText = response.text.encode('utf8')
    jsonDict = json.loads(jsonText)
    imageString = jsonDict["image"]
    bioString = jsonDict["summary"]
    if bioString == "":
        bioString = "N/A"
    return [imageString,bioString]


def getAvgRatings(name):
    ratings = dict()
    cur = g.db.cursor()
    toExecute = f"""SELECT averageRating, startYear FROM ratings INNER JOIN crew 
ON ratings.tconst==crew.id
INNER JOIN basics ON ratings.tconst==basics.tconst
WHERE crew.p == '{name}'
ORDER BY startYear"""
    cur.execute(toExecute)
    for row in cur:
        year = int(row[1])
        avgRating = float(row[0])
        if year not in ratings:
            ratings[year]=avgRating
        else:
            ratings[year]+=avgRating
            ratings[year]/=2
    ratings = [[ratings[rating],rating] for rating in ratings]
    return ratings

def getTopRatedMovies(name):
    cur = g.db.cursor()
    toExecute = f"""SELECT averageRating, primaryTitle FROM ratings INNER JOIN crew 
ON ratings.tconst==crew.id
INNER JOIN basics ON ratings.tconst==basics.tconst
WHERE crew.p == '{name}' AND crew.profession=='director'
ORDER BY averageRating DESC"""
    cur.execute(toExecute)
    topMovies = []
    i=0
    for row in cur:
        if i >=10:
            break
        topMovies.append(row)
        i+=1
    return topMovies

def getActors(name):
    cur = g.db.cursor()
    toExecute = f"""SELECT primaryName, COUNT(nconst) FROM nameBasics 
INNER JOIN crew ON nameBasics.title=crew.id
WHERE crew.p=='{name}' AND (nameBasics.profession='actor' OR nameBasics.profession='actress') GROUP BY nconst ORDER BY COUNT(nconst) DESC"""
    cur.execute(toExecute)
    favActors = []
    i=0
    for row in cur:
        if i >=10:
            break
        favActors.append(row)
    return favActors

def getProfit(name):
    xAxis = []
    yAxis = []
    toQuery=[]
    cur = g.db.cursor()
    toExecute = f"""SELECT DISTINCT primaryTitle, id FROM basics INNER JOIN crew ON basics.tconst=crew.id
WHERE crew.p='{name}' ORDER BY basics.startYear"""
    cur.execute(toExecute)
    for row in cur:
        xAxis.append(row[0])
        toQuery.append(row[1])
    # for id in toQuery:
    #     url = f"https://imdb-api.com/en/API/Title/k_djtd4542/{id}"
    #     payload = {}
    #     headers= {}
    #     response = requests.request("GET", url, headers=headers, data = payload)
    #     jsonText = response.text.encode('utf8')
    #     jsonDict = json.loads(jsonText)
    #     moneyString = jsonDict["boxOffice"]["cumulativeWorldwideGross"]
    #     if moneyString == "":
    #         yAxis.append(0)
    #     else:
    #         newY = ""
    #         for i in  moneyString:
    #             if i in "0123456789":
    #                 newY+=i
    #         yAxis.append(int(newY))
    return[xAxis,toQuery]

app = Flask(__name__)

def connect_db():
    return sqlite3.connect('imdbDB.db')




@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()


@app.route('/director/<name>')
def directorSite(name):
    toSend = dict()
    toSend["topMovies"] = getTopRatedMovies(name)
    toSend["ratingOverTime"] = getAvgRatings(name)
    toSend["profitOverTime"] = getProfit(name)
    toSend["favActors"] = getActors(name)
    toSend["fullName"] = getFullName(name)
    toSend["bioImg"] = getBioImage(name)
    return render_template("directorPage.html",toSend=toSend)

@app.route('/')
def home():
    cur = g.db.cursor()
    cur.execute("""SELECT DISTINCT nameBasics.primaryName, crew.p FROM nameBasics, crew 
    WHERE crew.p==nameBasics.nconst AND crew.profession=='director'""")
    usersArr = []
    idsArr = []
    a = []
    for row in cur:
        a.append((row[0],row[1]))
    return render_template('main.html', wats=a)
