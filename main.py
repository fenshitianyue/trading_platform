#!/usr/bin/python2
# coding:utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
import json
import MySQLdb

app = Flask(__name__)

# 网站主页面
# @app.route('/index')
# def login():
#     userName = request.values.get('name')
#     toolName = request.values.get('tool_name')
#     return render_template('index.html')

# 登陆主界面
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user/login', methods=['POST'])
def user_login():
    username = request.values.get('username')
    password = request.values.get('password')
    code = request.values.get('code')
    # return jsonify(code=1, msg='登陆失败，请重试!')
    return jsonify(code=0)

# 注册主界面
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
    sql = "select dev_name from dev where dev_name = '" + username + "'"
    # 执行查询操作
    cursor.execute(sql)
    result = cursor.fetchall()
    if result: # 如果查询结果不为空, valid = False
        return jsonify(valid=False)
    else:
        return jsonify(valid=True)

# 注册和后端交互逻辑
@app.route('/user/register', methods=['POST'])
def user_register():
    '''
    业务逻辑：
        1.从前端获取注册的各项信息
        2.将各项信息插入到数据库相应表中
        3.根据插入成功与否，给前端ajax返回相应的对象内容
    '''
    # 从前端获取数据
    data = request.get_json()
    data = json.loads(request.get_data())
    username = data['username']
    password = data['password'] # 用户密码 (string)
    workStatus = data['workStatus'] # 工作状态 (int)
    realName = data['realName'] # 真实姓名 (string) 编码是unocode,查看需要decode
    school = data['school'] # 学校名 (string) 编码是unocode,查看需要decode
    company = data['company'] # 公司名 (string) 编码是unocode,查看需要decode
    QQId = data['QQId'] # 通讯软件账号 (string)
    research = data['research'] # 研究方向 (string) 编码是unocode,查看需要decode
    education = data['education'] # 教育水平 (string) 编码是unocode,查看需要decode
    phone = data['phone'] # 手机号 (string)
    inviteCode = data['inviteCode'] # 邀请码 (string)
    # nation = data['nation'] # 手机号所属区域 (int)

    # # 连接MySQL数据库并获取到数据库句柄
    # db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    # cursor = db.cursor()
    # # 拼接SQL语句
    # sql = ""
    # # 执行插入操作
    # cursor.execute(sql)
    # result = cursor.fetchall()
    # if result: # 如果登陆成功，code=0
    #     return jsonify(code=0, msg="register OK")
    # else:
    #     return jsonify(code=1, msg="register Error") # TODO：暂时不考虑注册失败的原因，同意返回register Error
    return jsonify(username, password, workStatus, realName, school, company, QQId, research, education, phone, inviteCode)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

