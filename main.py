#!/usr/bin/python2
# coding:utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import Response
import json
import MySQLdb
import os

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)

# 网站主页面
@app.route('/main')
def main():
    username = '赵满刚'
    return render_template('index.html', name=username)

# 登陆主界面
@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user/login', methods=['POST'])
def user_login():
    username = request.values.get('username')
    password = request.values.get('password')
    code = request.values.get('code')
    #TODO:从数据库中查找是否存在用户名并且用户名是否和密码吻合
    #TODO:验证验证码是否正确
    # return jsonify(code=1, msg='登陆失败，请重试!')
    return jsonify(code=0)

# TODO:登陆时获取验证码
@app.route('/admin/getCaptcha')
def get_captcha():
    pass

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
    sql = "select dev_username from dev where dev_username = '" + username + "'"
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
    # # TODO:拼接SQL语句
    # sql = "insert into dev values("
    # # 执行插入操作
    # cursor.execute(sql)
    # result = cursor.fetchall()
    if True: # 如果登陆成功，code=0
        return jsonify(code=0, msg="register OK")
    else:
        return jsonify(code=1, msg="register Error") # TODO：暂时不考虑注册失败的原因，同意返回register Error

# 修改密码
@app.route('/resetPwd', methods=['POST'])
def resetPwd():
    # 从前端获取密码
    passwd = request.values.get('password')
    # 连接数据库
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    # 拼接sql语句
    sql = "update dev set dev_passwd = '" + passwd + "'"
    # 执行更新表 dev 操作
    cursor.execute(sql)
    result = cursor.fetchall()
    if result:
        return jsonify(code=0, msg="Password updated successfully")
    else:
        return jsonify(code=1, msg="Password updated failed") # TODO:暂时错误返回消息定为这个，后期细化错误原因
# 接订单
@app.route('/assignList', methods=['POST'])
def assignList():
    pass

# 返回图片
# 图片类型暂时都定为jpeg
@app.route('/images/<image_name>')
def get_image(image_name):
    imgPath = './static/images/' + image_name
    mime = 'image/jpeg'
    if not os.path.exists(imgPath):
        return jsonify("Image not found")
    with open(imgPath, 'rb') as f:
        image = f.read()
    return Response(image, mimetype=mime)

# 其他页面
@app.route('/main.html')
def templates_main():
    return render_template('main.html')

@app.route('/assignList.html')
def templates_assignList():
    return render_template('assignList.html')

@app.route('/myOrders.html')
def templates_myorders():
    return render_template('myOrders.html')

@app.route('/finishOrders.html')
def templates_finishorders():
    return render_template('finishOrders.html')

@app.route('/settleList.html')
def templates_settlelist():
    return render_template('settleList.html')

@app.route('/finishList.html')
def templates_finishList():
    return render_template('finishList.html')

@app.route('/myInvite.html')
def templates_myInvite():
    return render_template('myInvite.html')

@app.route('/myReward.html')
def templates_myreword():
    return render_template('myReward.html')

@app.route('/list.html')
def templates_list():
    return render_template('list.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

