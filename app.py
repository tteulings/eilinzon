from flask import Flask, redirect, render_template, request, session, url_for, jsonify, json, send_file
from flask_basicauth import BasicAuth
from datetime import date, datetime

import collections
import json
import os, random

from google_calendar import list_events, create_event


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = ''
app.config['BASIC_AUTH_PASSWORD'] = '108'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)


username="Familie"

@app.route('/',methods=["GET", "POST"])
def start():
    if request.method == "POST":
        description = request.form["description"]
        start, end = str(request.form["daterange"]).split(" tot ")

        create_event.create_event(start, end , description)

    with open("boodschappenlijst.json") as json_file:
        sl_items = json.load(json_file)
        order_items = collections.OrderedDict(reversed(list(sl_items.items())))

    with open("logboek.json") as json_file:
        log_items = json.load(json_file)
        log_items = collections.OrderedDict(reversed(list(log_items.items())))


    background_img = random.choice(os.listdir("./static/img"))
    return render_template("index.html", sl_items=order_items, log_items=log_items, background_img=background_img)


@app.route('/informatie', methods=["GET", "POST"])
def informatie():


    return render_template("informatie.html")


@app.route('/calendar', methods=["GET", "POST"])
def calendar():
    if request.method == "POST":
        description = request.form["description"]
        start = str(request.form["start"])
        end = str(request.form["end"])

        create_event.create_event(start,end,description)

    return render_template("calendar.html")


@app.route('/shopping_list', methods=["GET", "POST"])
def shopping_list():

    if request.method == "POST":
        with open("logboek.json", mode="r") as json_file:
            sl_items = json.load(json_file)

        sl_items[request.form["new_item_item"]] = {
            "user" : request.form["new_item_user"],
            "datetime" : "{}".format(date.today()),
            "quantity" : request.form["new_item_quantity"]
        }

        with open("logboek.json", mode="w") as output_file:
            json.dump(sl_items, output_file)

    with open("logboek.json") as json_file:
        sl_items = json.load(json_file)

        order_items = collections.OrderedDict(reversed(list(sl_items.items())))


    return render_template("shopping_list.html", sl_items=order_items, username=username)


@app.route('/add', methods=["GET", "POST"])
def add_to_list():

    with open("boodschappenlijst.json", mode="r") as json_file:
        sl_items = json.load(json_file)

    date_cur = datetime.strftime(date.today(), '%d-%m-%Y')

    new_item = {request.args.get('item') : {
        "user" : request.args.get('user'),
        "datetime" : date_cur,
        "quantity" : 1
    }}

    sl_items.update(new_item)

    with open("boodschappenlijst.json", mode="w") as output_file:
        json.dump(sl_items, output_file)

    return jsonify(new_item)

@app.route('/add_log', methods=["GET", "POST"])
def add_log():

    with open("logboek.json", mode="r") as json_file:
        log_items = json.load(json_file)

    if list(log_items.keys()):
        key = int(list(log_items.keys())[-1]) + 1
    else:
        key = 0

    new_item = {key : {
        "author" : request.args.get('author'),
        "datetime" : request.args.get('datetime'),
        "description" : request.args.get('description')
    }}


    log_items.update(new_item)

    with open("logboek.json", mode="w") as output_file:
        json.dump(log_items, output_file)

    return jsonify(new_item)

@app.route('/remove', methods=["GET", "POST"])
def remove_from_list():
    with open("boodschappenlijst.json", mode="r") as json_file:
        sl_items = json.load(json_file)

    sl_items.pop(request.args.get('item'))

    with open("boodschappenlijst.json", mode="w") as output_file:
        json.dump(sl_items, output_file)

    return jsonify("")

if __name__ == '__main__':
    app.run(debug=True)
