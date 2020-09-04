#!/usr/bin/env python

# -*- coding: utf-8 -*-

"""
###########################################################################
#
#   Project Name:   Leanna Joke Bot
#   Project Date:   Mar, 2020
#   Purpose:        Not go stir crazy during COVID-19 so thought that I 
#                   would build a bot to tell jokes and then share it with
                    Christele
#
###########################################################################
"""

__author__ = ["Nathaniel Vala", ]
__copyright__ = "Copyright 2020, Spydernaz"
__credits__ = ["Nathaniel Vala"]
__liciense__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = ["Nathaniel Vala"]
__email__ = ["nathanielvala","@", "hotmail","com"]
__status__ = "Dev"

from flask import Flask, render_template, request
import random, requests, json
import jokes
app = Flask(__name__)

key = 'a81e328ace2647de94814c97a26df167' # your Runtime key
endpoint = 'westus.api.cognitive.microsoft.com' # such as 'your-resource-name.api.cognitive.microsoft.com'
appId = '99a8674f-2710-4bf9-982a-845b26acbe2f'

luis_enabled = False

def getjoke():
    jokeid = random.randint(1,len(jokes.jokes))
    # Check for category

    joke = str(jokes.jokes[jokeid]["setup"] + " \r\n " + jokes.jokes[jokeid]["punchline"])
    return joke


@app.route("/")
def home():
    return render_template("button.html")

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')

    if luis_enabled:
        params ={
            'query': request.args.get('msg'),
            'timezoneOffset': '0',
            'verbose': 'true',
            'show-all-intents': 'true',
            'spellCheck': 'false',
            'staging': 'false',
            'subscription-key': key
        }

        r = requests.get(f'https://westus.api.cognitive.microsoft.com/luis/prediction/v3.0/apps/{appId}/slots/production/predict',headers={}, params=params)
        
        topIntent = r.json()["prediction"]["topIntent"]
        if r.json()["prediction"]["intents"][topIntent]["score"] > 0.85:
            intent = topIntent
        else:
            intent = None
    elif "joke" in request.args.get('msg'):
        intent = "ask for a joke"
    else:
        intent = "other"

    if intent == "ask for a joke":
        return getjoke()
    elif intent == "conversation":
        return "sorry, I cant really do conversations yet"
    else:
        return "sorry, I can only tell you a joke if you ask for one (and that is all I can do at the moment)"



@app.route("/getJokeButton")
def get_new_joke():
    jokeid = random.randint(1,len(jokes.jokes))
    # Check for category

    joke = jokes.jokes[jokeid]
    print(json.dumps(joke))
    return json.dumps(joke)

if __name__ == "__main__":
    app.run(debug=True)