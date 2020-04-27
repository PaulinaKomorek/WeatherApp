from flask import Flask, render_template, request
import requests
import json

app = Flask(__name__)

def get_apikey():
    with open("key.txt", "r") as keyfile:
        return keyfile.read()

key = get_apikey()
url = "http://api.openweathermap.org/data/2.5/weather?units=metric&"


def set_history(history: list):
    file_data=open("history.json", "w" )
    json.dump(history, file_data)
    file_data.close()
    



def get_history():
    file_data=open("history.json", "r" )
    history=json.load(file_data)        
    file_data.close()
    return history
    


@app.route("/", methods=["get"])
def index():
    getting_history=get_history()
    show_history=len(getting_history)>2
    return render_template("index.html", show_history=len(getting_history)>2, history_data=getting_history)


@app.route("/weather", methods=["get"])
def city_weather():
    user_city=request.args.get("selected_city")
    response = requests.get(url+"q=" + user_city + "&appid="+key)
    if  not response.ok:
         return render_template("error_occured.html")
    data = response.json()
    getting_history=get_history()
    getting_history.append([user_city.title(), data])
    if len(getting_history)>3:
        getting_history.pop(0)
    set_history(getting_history)
    return render_template("city_weather.html", city=user_city.title(), main=data["main"], icon=data["weather"][0]["icon"])


    

   