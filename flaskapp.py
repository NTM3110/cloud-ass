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
# import boto3
# import config as keys
# from boto3.dynamodb.conditions import Key, Attr
from controller.UserController import UserController
# Get the service resource.



app = Flask(__name__)


@app.route('/')
def root():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/checkRegister', methods = ['POST'])
def checkRegister():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # table = dynamodb.Table('login0')
            
        # table = dynamodb.Table('login0')
            
        # table.put_item(
        #     Item={
        #         'username': username,
        #         'email': email,
        #         'password': password
        #     }
        # ) 
        UserController.post_table()
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
        name = items[0]['username']
        print(items[0]['username'])
        print(items[0]['password'])
        if (password == items[0]['password'] and email == items[0]['email']):
            print('SUCCEED LOGIN')
            return render_template("main.html",name = name)
        print('Not correct')
    print('Fail')
    return render_template("login.html")

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
