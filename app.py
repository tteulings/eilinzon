from flask import Flask, redirect, render_template, request, session, url_for, jsonify, json
from flask_basicauth import BasicAuth
from datetime import date, datetime

import collections

from google_calendar import list_events, create_event
# from flask_sqlalchemy import SQLAlchemy
# import datetime, timeago, time

import json

app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'tet'
app.config['BASIC_AUTH_PASSWORD'] = 'tet'
app.config['BASIC_AUTH_FORCE'] = True

basic_auth = BasicAuth(app)

username="Familie"

@app.route('/',methods=["GET", "POST"])
def start():
    if request.method == "POST":
        print(request.form)
        description = request.form["description"]
        start = str(request.form["start"])
        end = str(request.form["end"])

        print(start)
        create_event.create_event(start,end,description)

    with open("logboek.json") as json_file:
        sl_items = json.load(json_file)
        order_items = collections.OrderedDict(reversed(list(sl_items.items())))


    return render_template("index.html", sl_items=order_items)

@app.route('/calendar', methods=["GET", "POST"])
def calendar():
    if request.method == "POST":
        print(request.form)
        description = request.form["description"]
        start = str(request.form["start"])
        end = str(request.form["end"])

        print(start)
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

    with open("logboek.json", mode="r") as json_file:
        sl_items = json.load(json_file)

    new_item = {request.args.get('item') : {
        "user" : request.args.get('user'),
        "datetime" : "{}".format(date.today()),
        "quantity" : request.args.get('quantity')
    }}

    sl_items.update(new_item)

    with open("logboek.json", mode="w") as output_file:
        json.dump(sl_items, output_file)

    return jsonify(new_item)

@app.route('/remove', methods=["GET", "POST"])
def remove_from_list():
    with open("logboek.json", mode="r") as json_file:
        sl_items = json.load(json_file)

    sl_items.pop(request.args.get('item'))

    with open("logboek.json", mode="w") as output_file:
        json.dump(sl_items, output_file)

    return jsonify("")

# @app.route('/agenda')
# def agenda():

#     return render_template("agenda.html")



# @app.route('/logboek', methods=["GET", "POST"])
# def logboek():

#     # if request.method == "POST":
#     #     return render_template("new_entry.html")



#     return render_template("logboek.html", messages=messages)

# @app.route('/new_entry', methods=["GET", "POST"])
# def new_entry():

#     if request.method == "POST":
#         with sqlite3.connect("logboek.db") as con:
#             cur = con.cursor()

#             start = request.form["start"]
#             end = request.form["end"]
#             message = request.form["entry"]

#             if not (start or end or message):
#                 return render_template("new_entry.html")

#             cur.execute("insert into logboekv2(start, end, user, message) values (?,?,?,?)", (start, end, "admin", message))

#         return redirect(url_for("logboek"))

#     return render_template("new_entry.html")


# @app.route('/to_do', methods=["GET", "POST"])
# def to_do():
#     if request.method == "POST":
#         if request.form["add_btn"] == "add":
#             print("test")

#             add_to_do()
#         elif request.form["rmv_btn"] == "rmv":
#             print("test")


#     with sqlite3.connect("to_do.db") as con:
#         cur = con.cursor()
#         cur.execute("select * from to_do")

#         fetchs  = cur.fetchall()

#         items = []
#         for fetch in fetchs:
#             item = {}

#             item["date"] = timeago.format(str(fetch[1][:-7]))
#             item["user"] = str(fetch[2])
#             item["item"] = str(fetch[3])

#             items.insert(0, item)


#     return render_template("to_do.html", to_dos=items)

# def add_to_do():
#     with sqlite3.connect("to_do.db") as con:
#             cur = con.cursor()

#             item = request.form["item"]

#             cur.execute("insert into to_do(date, user, item) values (?,?,?)", (str(datetime.datetime.now()), "admin", item))

#     return redirect(url_for("to_do"))

if __name__ == '__main__':
    app.run(debug=True)
