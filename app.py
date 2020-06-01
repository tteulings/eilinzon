from flask import Flask, redirect, render_template, request, session, url_for, jsonify, json, send_file
from flask_basicauth import BasicAuth
from flask_mail import Mail, Message

from datetime import date, datetime, timedelta
import collections, json, os, random
import atexit

from apscheduler.schedulers.background import BackgroundScheduler

from src.Events import get_events
from src.SendMail import send_mail, send_mails, check_arrival_mail, check_leave_mail
from src.VisitorsMails import get_visitors


from google_calendar import list_events, create_event


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = ''
app.config['BASIC_AUTH_PASSWORD'] = '108'
app.config['BASIC_AUTH_FORCE'] = True

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USERNAME'] = "eilinzon@gmail.com"
app.config['MAIL_PASSWORD'] = 'fuaebhpzqxhfvydg'

mail = Mail(app)
basic_auth = BasicAuth(app)


username = "Familie"

with app.app_context():
    scheduler = BackgroundScheduler()

scheduler.add_job(func=send_mails, args=[mail, app], trigger="cron", hour=12, minute=00)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())

@app.route('/', methods=["GET", "POST"])
def start():
    if request.method == "POST":
        description = request.form["description"]
        start, end = str(request.form["daterange"]).split(" tot ")

        create_event.create_event(start, end, description)

    with open("takenlijst.json") as json_file:
        tasks_items = json.load(json_file)
        order_tasks_items = collections.OrderedDict(
            reversed(list(tasks_items.items())))

    with open("boodschappenlijst2.0.json") as json_file:
        groc_items = json.load(json_file)
        order_groc_items = collections.OrderedDict(
            reversed(list(groc_items.items())))

    with open("logboek.json") as json_file:
        log_items = json.load(json_file)
        log_items = collections.OrderedDict(reversed(list(log_items.items())))

    background_img = random.choice(os.listdir("./static/img"))
    return render_template("index.html", tasks_items=order_tasks_items, groc_items=order_groc_items, log_items=log_items, background_img=background_img)


@app.route('/get_items', methods=["GET", "POST"])
def get_items():
    mode = request.args.get('mode')

    if mode == "tasks":
        file = "takenlijst.json"
    else:
        file = "boodschappenlijst2.0.json"

    with open(file) as json_file:
        mail_items = json.load(json_file)

        for item in mail_items.keys():
            mail_items[item].update({"item": item})

        order_items = list(
            reversed(list([item[1] for item in mail_items.items()])))
    return json.dumps({"items": order_items})


@app.route('/informatie', methods=["GET", "POST"])
def informatie():
    return render_template("informatie.html")

@app.route('/mails', methods=["GET", "POST"])
def mails():
    with open("mails.json") as json_file:
        mail_adresses = json.load(json_file)

    return render_template("mails.html", mail_adresses=mail_adresses)


@app.route("/mail")
def mail_route():
    send_mails(mail, app)

    return "succes"


@app.route('/add', methods=["GET", "POST"])
def add_to_list():
    mode = request.args.get('mode')

    if mode == "tasks":
        file = "takenlijst.json"
    else:
        file = "boodschappenlijst2.0.json"

    with open(file, mode="r") as json_file:
        mail_items = json.load(json_file)

    date_cur = datetime.strftime(date.today(), '%d-%m-%Y')

    new_item = {request.args.get('item'): {
        "user": request.args.get('user'),
        "datetime": date_cur,
        "quantity": 1,
        "item": request.args.get('item')
    }}

    mail_items.update(new_item)

    with open(file, mode="w") as output_file:
        json.dump(mail_items, output_file)

    return jsonify(new_item)

@app.route('/add_mail', methods=["GET", "POST"])
def add_mail():

    file = "mails.json"

    with open(file, mode="r") as json_file:
        mail_items = json.load(json_file)


    new_mail = {request.args.get('name'): request.args.get('mail')}
    mail_items.update(new_mail)

    with open(file, mode="w") as output_file:
        json.dump(mail_items, output_file)

    return jsonify(new_mail)

@app.route('/remove_mail', methods=["GET", "POST"])
def remove_mail():
    file = "mails.json"
    
    with open(file, mode="r") as json_file:
        mail_items = json.load(json_file)

    mail_items.pop(request.args.get('mail'))

    with open(file, mode="w") as output_file:
        json.dump(mail_items, output_file)

    return jsonify("")    


@app.route('/get_mails', methods=["GET", "POST"])
def get_mails():
    file = "mails.json"
    
    with open(file, mode="r") as json_file:
        mail_items = json.load(json_file)


        # order_items = list(
        #     reversed(list([item[1] for item in mail_items.items()])))
    return json.dumps({"items": mail_items})

@app.route('/add_log', methods=["GET", "POST"])
def add_log():

    with open("logboek.json", mode="r") as json_file:
        log_items = json.load(json_file)

    if list(log_items.keys()):
        key = int(list(log_items.keys())[-1]) + 1
    else:
        key = 0

    new_item = {key: {
        "author": request.args.get('author'),
        "datetime": request.args.get('datetime'),
        "description": request.args.get('description')
    }}

    log_items.update(new_item)

    with open("logboek.json", mode="w") as output_file:
        json.dump(log_items, output_file)

    return jsonify(new_item)


@app.route('/remove', methods=["GET", "POST"])
def remove_from_list():
    mode = request.args.get('mode')

    if mode == "tasks":
        file = "takenlijst.json"
    else:
        file = "boodschappenlijst2.0.json"
    print(file)
    with open(file, mode="r") as json_file:
        mail_items = json.load(json_file)

    mail_items.pop(request.args.get('item'))
    print(request.args.get('item'))

    with open(file, mode="w") as output_file:
        json.dump(mail_items, output_file)

    return jsonify("")


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
