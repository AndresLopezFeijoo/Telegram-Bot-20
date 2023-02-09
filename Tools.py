import os
import csv
import json
from datetime import date
from telegram import InlineKeyboardButton
import smtplib, ssl
from email.message import EmailMessage
from collections import Counter


password = json.load(open("token.json"))["gmail2"]


def send_mail(mens):
    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("astorito.bot@gmail.com", password)
        msg = EmailMessage()
        msg.set_content(mens)
        msg['Subject'] = 'Reporte'
        msg['From'] = "astorito.bot@gmail.com"
        msg['To'] = "astorito.bot@gmail.com"
        server.send_message(msg)


def slice_lst(lst, lst2, step):
    for i in range(0, len(lst), step):
        lst2.append(lst[i:i+step])
    return lst2


def get_lst(path, clear: bool, nr: bool):  # Clear quita las extensiones, nr devuelce ints
    if clear:
        lst = [i.split(".")[0] for i in os.listdir(path) if not i.startswith('.')]
        if nr:
            lst = [int(i.split(".")[0]) for i in os.listdir(path) if not i.startswith('.')]
    else:
        lst = [i for i in os.listdir(path) if not i.startswith('.')]

    return sorted(lst)


def base_key(*args, two: bool):
    if two:
        keyboard = [[InlineKeyboardButton("Terminar", callback_data="end"),
                     InlineKeyboardButton("Home", callback_data="home")]]
    else:
        keyboard = [[InlineKeyboardButton(args[0], callback_data=args[1])],
                    [InlineKeyboardButton("Home", callback_data="home"),
                     InlineKeyboardButton("Terminar", callback_data="end")]]
    return keyboard

def print_folder(path):
    i = json.dumps(get_lst(path, True, False))
    return print(i)

#print_folder("/Users/andreslopezfeijoo/Desktop/Para Agregar a astorito/Bajo Dado/5dimaumResuel")