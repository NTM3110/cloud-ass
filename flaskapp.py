# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from flask import Flask, render_template,request
import json
# import boto3
# import config as keys
# from boto3.dynamodb.conditions import Key, Attr
from controller.UserController import UserController
from controller.MusicController import MusicController
from controller.S3Controller import S3Controller
# Get the service resource.



app = Flask(__name__)
def render():
    title = request.form['title']
    print(title)
    items = MusicController.get_item(title)
    print(items[0])
    render_template('main.html',data = items)

@app.route('/')
def root():
    response = MusicController.create_table()
    if response == False:
        f = open('a1.json')
        data = json.load(f)
        for song in data['songs']:
            print(song['title'])
            MusicController.post_table(song['title'],song['artist'],song['year'],song['web_url'],song['img_url'])
    return render_template('login.html')

@app.route('/query', methods = ['POST'])
def query():
    if request.method == 'POST':
        title = request.form['title']
        name = request.form['name']
        print(name)
        items = MusicController.get_item(title)
        music_img = S3Controller.show_image("song-image")
        return render_template('main.html',data = items, name = name,images = music_img)
    return render_template('main.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/checkRegister', methods = ['POST'])
def checkRegister():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        UserController.post_table(username,email,password)
        msg = "Registration Complete. Please Login to your account !"
        return render_template('login.html',msg = msg)
    return render_template('register.html')


@app.route("/checkLogin", methods = ['POST'])
def checkLogin(): 
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        # table = dynamodb.Table('login0')
        # response = table.query(
        #         KeyConditionExpression=Key('email').eq(email)
        # )
        items = UserController.check(email)
        if len(items) != 0:
            name = items[0]['username']
            print(items[0]['username'])
            print(items[0]['password'])
            if (password == items[0]['password'] and email == items[0]['email']):
                print('SUCCEED LOGIN')
                music_data = MusicController.get_all_item()
                music_img = S3Controller.show_image("song-image")
                
                return render_template("main.html",name = name,data = music_data,images = music_img)
            print('Not correct')
    print('Fail')
    msg = "Email or password is invalid"
    return render_template("login.html",msg = msg)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8081, debug=True)
# [END gae_python3_render_template]
# [END gae_python38_render_template]
