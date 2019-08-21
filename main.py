#!/usr/bin/python2
# coding:utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import Response
from flask import session
from datetime import timedelta
import json
import MySQLdb
import os
import random
import base64
import gvcode
from cStringIO import StringIO

import sys
reload(sys)
sys.setdefaultencoding('utf8')

app = Flask(__name__)
app.config['SECRET_KEY'] = '654321'  # 使用session前设置密匙
app.config['PREMANENT_SESSION_LIFETIME'] = timedelta(days=7)  # 设置session的过期时间

# 网站主页面
@app.route('/main')
def main():
    # 从session获取username
    username = session.get('username', None)
    # 如果成功从session中获取到username，那么返回主页
    if username:
        return render_template('index.html', name=username)
    else:  # 如果session中不存在username，那么返回登陆页面
        return render_template('login.html')

# 登陆主界面
@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/user/login', methods=['POST'])
def user_login():
    username = request.values.get('username')
    password = request.values.get('password')
    code = request.values.get('code')
    # 从 session 获取正确验证码
    correct_code = session.get('code', None)
    # 从数据库中查找是否存在用户名和密码
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    sql = "select dev_username, dev_passwd from dev where dev_username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchone()
    # 用户名是否存在?
    if not result:
        return jsonify(code=1, msg='用户名不存在！')
    else:
        dev_passwd = result[1]
        # 用户名和密码是否吻合?
        if dev_passwd != password:
            return jsonify(code=1, msg='密码错误！')

    # 如果可以用户可以正常登陆，将用户名写入session
    session['username'] = username
    # 比对用户填写的用户码和正确验证码是否一致
    if code.lower() != correct_code.lower():
        return jsonify(code=1, msg='验证码错误！')
    db.close()
    return jsonify(code=0)

# 登陆时获取验证码
@app.route('/admin/getCaptcha', methods=['GET', 'POST'])
def get_captcha():
    # 生成验证码并发送给前端
    img, code = gvcode.generate(size=(80, 27), length=4)
    session['code'] = code  # 将生成的验证码数据存入session
    out = StringIO()
    img.save(out, format='PNG')
    b64 = base64.b64encode(out.getvalue())
    result = "data:image/png;base64,"
    result = result + b64
    return result

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
    db.close()
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
    username = data['username'] # 用户名 (string)
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
    # nation = data['nation'] # 手机号所属区域 (int) TODO:暂不考虑，统一插入0
    # 新用户的邀请码
    newInviteCode = generate_invite_code()
    # # 连接MySQL数据库并获取到数据库句柄
    # db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    # cursor = db.cursor()
    # # 检测是否填写邀请码
    # if inviteCode:
    #     # TODO:在数据库中查询邀请码是否正确
    #     sql_s = ""
    #     try:
    #         cursor.execute(sql_s)
    #     except:
    #         return jsonify(code=1, msg="检查所填写的邀请码是否正确！")

    # sql_i = "insert into dev() values("

    # sql_i = sql_i + ")"
    # # 执行插入操作
    # cursor.execute(sql_i)
    # result = cursor.fetchall()
    if True:
        return jsonify(code=0, msg="register OK")  # 如果注册成功，code=0
    else:
        return jsonify(code=1, msg="register Error")  # TODO：暂时不考虑注册失败的原因，后期再考虑细化失败原因

# 修改密码
@app.route('/resetPwd', methods=['POST'])
def resetPwd():
    # 从session获取username
    username = session.get('username', None)
    # 从前端获取密码
    passwd = request.values.get('password')
    # 连接数据库
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    # 更新数据库中当前用户的密码
    sql = "update dev set dev_passwd = '" + passwd + "'" + " where dev_username = '" + username + "'"
    cursor.execute(sql)
    db.commit()
    # 从数据库中查找当前用户的密码
    sql = "select dev_passwd from dev where dev_username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchone()
    dev_passwd = result[0]
    # 判断修改后的密码和新密码是否相同?
    db.close()
    if dev_passwd == passwd:
        return jsonify(code=0, msg="密码修改成功！")
    else:
        return jsonify(code=1, msg="密码修改失败！")  # TODO:暂时错误返回消息定为这个，后期细化错误原因

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

# 生成邀请码(6位大写字母)
def generate_invite_code():
    invite_code = ""
    for i in range(6):
        c = chr(random.randrange(65, 91))
        invite_code = invite_code + c
    return invite_code

# 安全退出
@app.route('/logout')
def logout():
    # 删除当前用户保存在session中的数据(username)
    session.pop('username')
    return render_template('login.html')

# 其他页面
@app.route('/main.html')
def templates_main():
    # 从session获取用户名
    username = session.get('username', None)
    # 从数据库查找用户名对应的真实姓名和邀请码
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    sql = "select dev_realname, dev_invitecode from dev where dev_username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchone()

    toolname = result[0]
    invite_code = result[1]

    db.close()
    return render_template('main.html', toolName=toolname, code=invite_code)

# 查询订单
@app.route('/assignList.html')
def templates_assignList():
    return render_template('assignList.html')

@app.route('/orders/assignList', methods=['GET', 'POST'])
def assignList():
    path_pre = "/home/zanda/Desktop/Project/trading_platform/"
    dict = {}
    dict['id'] = 4000
    dict['title'] = "基于Unix的微型操作系统"
    dict['publishTime'] = "20180810000000"
    dict['dueTime'] = "20190820000000"
    dict['orderTag'] = "C"
    dict['requireType'] = "操作系统"
    dict['devPrice'] = "$10000"
    dict['orderStatus'] = "辅导中"
    dict['docFilePath'] = path_pre + "document/doc/test.doc"
    dict['allFilePath'] = path_pre + "attachment/interface.zip"
    dict['requirement'] = "详细需求请联系(qq)：1262167092~"
    dict['devRemark'] = "请勿抄袭网上代码！"

    result = [dict]
    # data是一个列表，列表元素类型是字典
    return jsonify(total=1, data=result)

# 接订单
@app.route('/orders/pickOrder')
def pickOrder():
    pass

# 显示已完成订单
@app.route('/orders/finishOrders', methods=['POST'])
def finishOrders():
    pass

# 显示已接订单
@app.route('/myOrders.html')
def templates_myorders():
    return render_template('myOrders.html')

@app.route('/orders/myOrders', methods=['POST'])
def myOrders():
    pass

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

