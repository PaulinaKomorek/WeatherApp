from flask import Flask, render_template, request
import requests
import json
import numpy as np
import matplotlib.pyplot as plt
from math import *
import datetime
import random
import string
import matplotlib

app = Flask(__name__)


def get_apikey():
    with open("key.txt", "r") as keyfile:
        return keyfile.read()


key = get_apikey()
url = "http://api.openweathermap.org/data/2.5/weather?units=metric&"
historical_url = "https://samples.openweathermap.org/data/2.5/history/city?"


def set_history(history: list):
    file_data = open("history.json", "w")
    json.dump(history, file_data)
    file_data.close()


def get_history():
    file_data = open("history.json", "r")
    history = json.load(file_data)
    file_data.close()
    return history


def random_string(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def draw_plot(x, y):
    plt.ylabel('temperature [°C]').set_color("white")
    plt.xlabel("time").set_color("white")
    plt.tick_params(axis='both', colors='white')
    matplotlib.rc('axes', edgecolor='w')
    random_name = random_string()+".png"
    plt.xticks([0, 1, 2], x)
    plt.plot([0, 1, 2], y)
    plt.savefig("static/tmp/"+random_name, transparent=True)
    plt.clf()
    return random_name



@app.route("/", methods=["get"])
def index():
    getting_history = get_history()
    show_history = len(getting_history) > 2
    return render_template("index.html", show_history=len(getting_history) > 2, history_data=getting_history)


@app.route("/weather", methods=["get"])
def city_weather():
    user_city = request.args.get("selected_city")
    response = requests.get(url+"q=" + user_city +"&appid="+key)
    if not response.ok:
        return render_template("error_occured.html")
    historical_response = requests.get(
        historical_url+"q=" + user_city + "&appid="+key)
    historical_data = historical_response.json()
    historical_temp = [historical_data["list"][0]["main"]["temp"]-273, historical_data["list"]
                       [1]["main"]["temp"]-273, historical_data["list"][2]["main"]["temp"]-273]
    print(historical_url+"q=" + user_city + "&appid="+key)
    hour = datetime.datetime.now().hour
    hours = [(hour-2) % 24, (hour-1) % 24, hour % 24]
    data = response.json()
    getting_history = get_history()
    getting_history.append([user_city.title(), data])
    if len(getting_history) > 3:
        getting_history.pop(0)
    set_history(getting_history)
    return render_template("city_weather.html", city=user_city.title(), main=data["main"], icon=data["weather"][0]["icon"], filename=draw_plot(hours, historical_temp))

