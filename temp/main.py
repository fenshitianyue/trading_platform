#!/usr/bin/python2
# coding:UTF-8

from flask import Flask
from flask import render_template

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

@app.route('/login')
def login_tmp():
    return render_template('maintenance.html')

@app.route('/main')
def main_tmp():
    return render_template('maintenance.html')

@app.route('/register')
def register_tmp():
    return render_template('maintenance.html')

if __name__ == '__main__':
    app.run('0.0.0.0')
