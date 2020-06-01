from flask import Flask, redirect, render_template, request, session, url_for, jsonify, json, send_file
from flask_mail import Mail, Message
import codecs

from src.Events import get_events
from src.VisitorsMails import get_visitors


def send_mail(app, mail, visitors, visitors_mails, mode="starting"):
    print(visitors_mails)
    if not visitors_mails:
        msg = Message("Kan mail niet versturen Eilinzon",
                sender="eilinzon@gmail.com",
                recipients=["tijs.t@hotmail.com"])

        msg.body = "Bezoek Eilinzon"
        print("error")
        msg.html = f"Kan mail niet versturen naar {visitors}"
        
        with app.app_context():

            mail.send(msg)

        return 

    if mode == "starting":
        print(visitors, visitors_mails)
        msg = Message("Bezoek Eilinzon",
                        sender="eilinzon@gmail.com",
                        recipients=visitors_mails)

        # print(str(f"{codecs.open('templates/mail_templates/arrival_mail.html', 'r', 'utf-8').read()}"))
        msg.body = "Bezoek Eilinzon"
        msg.html = f"Beste {', '.join(visitors)} {codecs.open('templates/mail_templates/arrival_mail.html', 'r', 'utf-8').read()}"

        with app.app_context():
            mail.send(msg)

    if mode == "ending":
        print(visitors, visitors_mails)
        msg = Message("Vertrek Eilinzon",
                        sender="eilinzon@gmail.com",
                        recipients=visitors_mails)

        msg.body = "Vertrek Eilinzon"
        msg.html = f"Beste {', '.join(visitors)} {codecs.open('templates/mail_templates/leave_mail.html', 'r', 'utf-8').read()}"
        with app.app_context():
            mail.send(msg)


def send_mails(mail, app):
    ending_event, starting_event = get_events(24)

    if starting_event:
        visitors, visitors_mails = get_visitors(starting_event)

        send_mail(app, mail, visitors,visitors_mails, "starting")


    if ending_event:
        visitors, visitors_mails = get_visitors(ending_event)
        send_mail(app, mail, visitors,visitors_mails, "ending")


    return "succes"

def check_arrival_mail(mail,app):
    _, starting_event = get_events()
    
    if starting_event:
        visitors, visitors_mails = get_visitors(starting_event)

        send_mail(app, mail, visitors,visitors_mails, "starting")

def check_leave_mail(mail, app):
        ending_event, _ = get_events()

        if ending_event:
            visitors, visitors_mails = get_visitors(ending_event)
            send_mail(app, mail, visitors,visitors_mails, "ending")


