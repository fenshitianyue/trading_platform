#!/usr/bin/python
# coding:utf-8

from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

