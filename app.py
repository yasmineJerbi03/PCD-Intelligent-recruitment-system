import json
import base64
import requests 

import cv2, sys, os
import time
import numpy as np 

from flask import Flask, render_template, request
from flask import Response


app = Flask(__name__)
app.static_folder = 'static'



@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")



@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    username = request.args.get('username')
    r = requests.post("http://127.0.0.1:4000/chat", json={'input' : userText , 'username' : username})
    out = r.json()['output']
    return out 


#webapp smartsignin



@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video')
def video():
    return render_template("camera.html")

@app.route('/persons')
def persons():
    url = "http://192.168.232.128:49265/v1/telnetai/api/persons"
    headers = {'Content-type': 'application/json', 'bearer': token}
    r = requests.get(url,  headers=headers)
    liste = r.json()['persons']
    Persons = ""
    for i in range(len(liste)):
        Persons += "ID = " + str(liste[i][2]) + ", Name = " + liste[i][0] + ", Last Name = " + liste[i][1] + "\n"

    return Persons







API_ENDPOINT = "http://192.168.232.128:49265/v1/telnetai/api/signin/smart"
token ="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IndpZW0zMC5iZW5hbWV1ckBnbWFpbC5jb20iLCJleHAiOjE1OTgwMTQzOTQsImlhdCI6MTU5NzY1NDM5NCwiaXNzIjoiTWljcm8gU2VydmljZSAtIFNpZ25pbkFQSSIsInJvbGUiOiJVc2VyIn0.25EBtOtvIrckc58yABzyVHkKd607Eu0MAjgy5cXI7uY"


@app.route('/SmartSignin', methods=['POST'])
def SmartSignin():
    encoded_data = request.get_json(force=True)
    print(encoded_data)

    url = "http://192.168.232.128:49265/v1/telnetai/api/signin/smart"
    headers = {'Content-type': 'application/json', 'bearer': token}
    r = requests.post(API_ENDPOINT, data=encoded_data , headers=headers)
    print(r.json())

    if r.json()['message'] == 'access permitted!':
        with open('data.json') as json_file:
            data = json.load(json_file)
        for p in data['user']:
            if r.json()['name'] == p['name']:
                rr = requests.post('http://127.0.0.1:4000/chat',  json={'input': p['profil'], 'username': p['name']}, headers=headers)
                print( rr )
                return(r.json())

    return r.json()
    


#tabe of database
data = {}
data['user'] = []
data['user'].append({
    'name': 'wiem',
    'profil': 'web support'
    
})
data['user'].append({
    'name': 'hatem',
    'profil': 'iot support'
    
})
data['user'].append({
    'name': 'mohamed',
    'profil': 'mobile'
    
})

with open('data.json', 'w') as file:
    json.dump(data, file)




if __name__ == "__main__":
    app.run(host='0.0.0.0')

