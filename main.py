#!/usr/bin/python2
# coding:utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
# import json
import MySQLdb

app = Flask(__name__)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/user/checkUsername', methods=['POST'])
def checkUsername():
    '''
    业务逻辑：
        1.从前端ajax拿到username
        2.从MySQL数据库中查询username
        3.将查询对应的结果进行计算后返回给前端ajax
    '''
    # 从前端ajax拿到username
    username = request.values.get('username')
    # 连接MySQL数据库并获取到数据库句柄
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    # 拼接SQL语句
    sql = ''
    # 执行查询操作
    cursor.execute(sql)
    result = cursor.fetchall()
    if result: # 如果查询结果不为空, valid = False
        return jsonify(valid=False)
    else:
        return jsonify(valid=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
