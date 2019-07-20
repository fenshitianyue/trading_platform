#!/usr/bin/python
# coding:utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import make_response

app = Flask(__name__)

@app.route('/')
def test():
    '测试函数'
    result = 'method:' + request.method  + 'url:' + request.url
    # for key, value in request.headers:
    #     result += '[' + key + ':' + value + ']'
    # response = make_response(render_template('hello_world.html', hello=result), 200)
    # response.headers['X-Something'] = 'A value'
    return render_template('hello_world.html', hello=result)

@app.route('/hello')
def hello():
    temp = 'hello world'
    return render_template('hello_world.html', hello=temp)

@app.route('/translate')
def translate():
    '翻译功能入口'

if __name__ == '__main__':
    '主函数入口'
    app.run(host='0.0.0.0', debug=True)
