#!/usr/bin/python2
# coding:utf-8

from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify
from flask import Response
from flask import session
from flask import redirect, url_for  # url重定向
from flask import send_from_directory  # 文件下载
from werkzeug import secure_filename # TODO:获取上传文件名
from datetime import timedelta
from datetime import datetime
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
app.config['PREMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # 设置session的过期时间

# 文件上传相关设置
UPLOAD_FOLDER = './document/doc/'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'doc', 'docx'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 网站主页面
@app.route('/main')
def main():
    # 从session获取username
    username = session.get('username', None)
    # 如果成功从session中获取到username，那么返回主页
    if username:
        return render_template('index.html', name=username)
    else:  # 如果session中不存在username，那么返回登陆页面
        return redirect(url_for('login'))

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
    print data['inviteCode']
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
    # return render_template('login.html')
    return redirect(url_for('login'))

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

# 文件下载
# TODO:如果文件名是中文的，这里可能会有问题
# TODO:如果需要下载的文件是pdf文件，可能需要另作一番处理
@app.route('/download/<path:filepath>', methods=['GET'])
def download(filepath):
    path_pre = "/home/zanda/Desktop/Project/trading_platform/"
    filepath = path_pre + filepath
    (dirname, filename) = os.path.split(filepath)
    return send_from_directory(dirname, filename, as_attachment=True)

# 查询订单
@app.route('/assignList.html')
def templates_assignList():
    return render_template('assignList.html')

@app.route('/orders/assignList', methods=['GET', 'POST'])
def assignList():
    '''
    业务逻辑：
        1.从前端获取有关分页的信息
        2.根据分页信息拼装SQL语句，在MySQL数据库中查找对应数据
        3.将查找到的数据拼接成json格式发送给前端
    '''
    path_pre = "/download/"
    # 从前端获取分页相关信息
    data = request.get_json()
    data = json.loads(request.get_data())
    pageNumber = data['pageNumber']
    pageSize = data['pageSize']
    # 连接数据库
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    # 先查询一下一共有多少条订单信息
    sql = "select count(*) from orders"
    cursor.execute(sql)
    num = cursor.fetchone()
    # 然后查询出当前页的订单信息
    sql = "select * from orders limit " + str((pageNumber-1) * pageSize) + "," + str(pageSize)
    cursor.execute(sql)
    # 根据查询结果拼接响应数据格式
    results = cursor.fetchall()
    if not results:
        return jsonify(total=0, data=[])
    response = []
    for row in results:
        dict = {}
        dict['id'] = row[0]
        dict['title'] = row[1]
        dict['publishTime'] = str(row[2])  # 对时间戳做一个处理
        dict['dueTime'] = str(row[3])  # 对时间戳做一个处理
        dict['orderTag'] = row[4]
        dict['requireType'] = row[5]
        dict['devPrice'] = row[6]
        if not row[7]:
            dict['docFilePath'] = ""
        else:
            dict['docFilePath'] = path_pre + row[7]
        if not row[8]:
            dict['allFilePath'] = ""
        else:
            dict['allFilePath'] = path_pre + row[8]
        dict['requirement'] = row[9]
        dict['devRemark'] = row[10]
        dict['orderStatus'] = row[11]
        dict['pickFlag'] = row[12]
        response.append(dict)
    db.close()
    return jsonify(total=num, data=response)

# 接订单
@app.route('/orders/pickOrder', methods=['POST'])
def pickOrder():
    '''
    业务逻辑：
        1.从前端获取订单号
        2.从session中获取当前开发者的username
        3.在(开发者-订单)表中插入对应的一条数据(username<->order_num)
        4.更新订单表中对应订单的状态
        5.更新当前用户开发中订单表
        6.拼接响应返回给前端
    '''
    order_num = request.values.get('id')
    # print "id:" + order_num
    username = session.get('username', None)
    # print "username:" + username

    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    # 更新订单对应表
    sql = "insert into trading(order_num, dev_username) values(" + str(order_num) + ",'" + username + "')"
    cursor.execute(sql)
    # TODO:这里可能要用异常判断一下commit是否成功
    db.commit()
    # 更新订单表
    sql = "update orders set order_status = '辅导中', order_flag = 1 where order_num = " + str(order_num)
    cursor.execute(sql)
    # TODO:这里可能要用异常判断一下commit是否成功
    db.commit()
    # TODO:更新当前用户开发中订单表
    db.close()
    # 根据查询结果拼接响应数据格式
    return jsonify(code=0, msg="接单成功！")

# 显示已接订单
@app.route('/myOrders.html')
def templates_myorders():
    return render_template('myOrders.html')

@app.route('/orders/myOrders', methods=['POST'])
def myOrders():
    '''
    业务逻辑(临时)：
        1.从session获取当前用户的username
        2.从trading表中查找当前用户所接订单的order_num
        3.根据获取到的order_num从orders表中查找对应订单信息
        4.将信息拼装成对应json格式发送给前端
    '''
    # TODO:先不做分页处理
    path_pre = "/download/"
    username = session.get('username', None)
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    # 更新订单对应表
    sql = "select order_num from trading where dev_username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    tmp = []
    for row in result:
        tmp.append(int(row[0]))
    num_set = tuple(tmp)
    sql = "select * from orders where order_num in " + str(num_set)
    sql = sql[0:-2]
    sql = sql + ")"
    cursor.execute(sql)
    results = cursor.fetchall()
    if not results:
        return jsonify(total=0, data=[])
    num = 0
    response = []
    for row in results:
        dict = {}
        dict['orderStatus'] = row[11]
        if dict['orderStatus'] == "辅导中":
            dict['orderStatus'] = "未完成"
        elif dict['orderStatus'] == "已完成":
            continue
        dict['id'] = row[0]
        dict['title'] = row[1]
        dict['publishTime'] = str(row[2])  # 对时间戳做一个处理
        dict['dueTime'] = str(row[3])  # 对时间戳做一个处理
        dict['orderTag'] = row[4]
        dict['requireType'] = row[5]
        dict['devPrice'] = row[6]
        if not row[7]:  # 如果文档路径不存在
            dict['docFilePath'] = ""
        else:
            dict['docFilePath'] = path_pre + row[7]
        if not row[8]:  # 如果附件路径不存在
            dict['allFilePath'] = ""
        else:
            dict['allFilePath'] = path_pre + row[8]
        dict['requirement'] = row[9]
        dict['devRemark'] = row[10]
        dict['pickFlag'] = row[12]
        response.append(dict)
        num += 1
    db.close()
    return jsonify(total=num, data=response)

# 显示已完成订单
@app.route('/finishOrders.html')
def templates_finishorders():
    return render_template('finishOrders.html')

@app.route('/orders/finishOrders', methods=['POST'])
def finishOrders():
    # TODO:先不做分页处理
    # 获取分页相关信息
    # data = request.get_json()
    # data = json.loads(request.get_data())
    # pageNumber = data['pageNumber']
    # pageSize = data['pageSize']
    # 获取当前用户
    username = session.get('username', None)
    # 连接数据库
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    sql = "select order_num from trading where dev_username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchall()
    tmp = []
    for row in result:
        tmp.append(int(row[0]))
    num_set = tuple(tmp)
    sql = "select * from orders where order_num in " + str(num_set)
    sql = sql[0:-2]
    sql = sql + ")"
    cursor.execute(sql)
    results = cursor.fetchall()
    if not results:
        return jsonify(total=0, data=[])
    response = []
    num = 0
    for row in results:
        dict = {}
        dict['orderStatus'] = row[11]
        if dict['orderStatus'] == "辅导中" or dict['orderStatus'] == "未完成":
            continue
        dict['id'] = row[0]
        dict['title'] = row[1]
        dict['publishTime'] = str(row[2])  # 对时间戳做一个处理
        dict['dueTime'] = str(row[3])  # 对时间戳做一个处理
        dict['orderTag'] = row[4]
        dict['requireType'] = row[5]
        dict['devPrice'] = row[6]
        # 申请状态只有 0:false/1:true
        if not row[13] or row[13] == 0:
            dict['billStatus'] = 0
        else:
            dict['billStatus'] = 1
        '''
        结算状态：
            0.申请等待售后
            1.未结算
            2.结算完成
            3.结算中
        '''
        if row[15] == 0:
            dict['isBillable'] = 0
        else:
            dict['isBillable'] = 1
        response.append(dict)
        num += 1
    db.close()
    return jsonify(total=num, data=response)

@app.route('/settleRecord/settle/<id>')
def settle_record(id):
    # 更新订单表中指定id订单的结算状态
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()

    sql = "update orders set order_appli = 1, order_settlement = 0 where order_num = " + str(id)
    cursor.execute(sql)
    db.commit()  # TODO:这里对commit应该做一个异常处理

    # 获取当前系统时间作为"申请时间"提交到数据库
    now_time = str(datetime.now())
    now_time = now_time[0:-7]
    sql = "update orders set order_appli_time = '" + now_time + "'" + " where order_num = " + str(id)
    cursor.execute(sql)
    db.commit()  # TODO:这里对commit应该做一个异常处理

    db.close()
    response = "申请结算成功!"
    return response

@app.route('/settleList.html')
def templates_settlelist():
    return render_template('settleList.html')

@app.route('/settleRecord/settleList', methods=['POST'])
def settle_list():
    # TODO:暂不做分页处理

    # 获取当前用户
    username = session.get('username', None)

    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()

    sql = "select order_num from trading where dev_username = '" + username + "'"
    cursor.execute(sql)
    result = cursor.fetchall()

    tmp = []
    for row in result:
        tmp.append(int(row[0]))
    num_set = tuple(tmp)
    sql = "select * from orders where order_num in " + str(num_set)
    sql = sql[0:-2]
    sql = sql + ")"
    cursor.execute(sql)
    results = cursor.fetchall()

    if not results:
        return jsonify(total=0, data=[])

    response = []
    num = 0
    for row in results:
        if row[11] == "辅导中" or row[11] == "未完成":
            continue
        dict = {}
        dict['orderId'] = row[0]
        dict['payType'] = row[16]
        if dict['payType'] == 1:
            dict['aliAccount'] = row[17]
        else:
            dict['backAccount'] = row[18]
        dict['payAccount'] = dict['payType']
        dict['totalFee'] = (int(row[6]) * 8) / 10  # 结算金额计算公式
        dict['applyTime'] = str(row[14])  # 对时间戳做一个处理
        dict['settleStatus'] = 0  # TODO
        response.append(dict)
        num += 1
    db.close()
    return jsonify(total=num, data=response)

@app.route('/finishList.html')
def templates_finishList():
    return render_template('finishList.html')

@app.route('/myInvite.html')
def templates_myInvite():
    return render_template('myInvite.html')

@app.route('/myReward.html')
def templates_myreword():
    return render_template('myReward.html')

# 消息通知
@app.route('/list.html')
def templates_list():
    return render_template('list.html')

@app.route('/notice/list', methods=['POST'])
def notice_list():
    '''
    业务逻辑：
        1.从前端获取分页的有关信息
        2.根据获取到的分页信息拼接SQL语句，从数据库查找订单记录
        3.将查到的结果拼装成json格式发送给前端
    '''
    # 从前端获取分页相关信息
    data = request.get_json()
    data = json.loads(request.get_data())
    pageNumber = data['pageNumber']
    pageSize = data['pageSize']
    # 连接数据库
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    # 先查询一下一共有多少条系统通知
    sql = "select count(*) from sys_notice"
    cursor.execute(sql)
    num = cursor.fetchone()
    # 然后查询出当前页的系统通知信息
    sql = "select * from sys_notice limit " + str((pageNumber-1) * pageSize) + "," + str(pageSize)
    cursor.execute(sql)
    # 根据查询结果拼接响应数据格式
    results = cursor.fetchall()
    if not results:
        return jsonify(total=0, data=[])
    response = []
    for row in results:
        tmp = {}
        tmp['id'] = row[0]
        tmp['title'] = row[1]
        tmp['content'] = row[2]
        # 对时间戳做一个处理
        tmp['createTime'] = str(row[3])
        tmp['status'] = row[4]
        response.append(tmp)
    db.close()
    # response = []
    # tmp = {}
    # tmp['id'] = 1
    # tmp['title'] = "测试标题"
    # tmp['content'] = "测试通知"
    # tmp['createTime'] = "2019-09-02 16:07:00"
    # tmp['status'] = 0
    # response.append(tmp)
    return jsonify(total=num, data=response)

# 消息已阅
@app.route('/notice/read/<id>', methods=['POST'])
def notice_read(id):
    '''
    业务逻辑：
        1.从url获取订单id
        2.修改数据库中对应订单的'阅读状态'字段
        3.将结果拼接成json格式发送给前端
    '''
    db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')
    cursor = db.cursor()
    sql = "update sys_notice set status=1 where id = " + str(id)
    cursor.execute(sql)
    # TODO:这里对commit应该做一个异常处理
    db.commit()
    db.close()
    return jsonify(code=0)

# TODO:文件上传
# 验证上传的文件名是否符合要求，文件名必须带点并且符合允许上传的文件类型要求
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.methods == 'POST':
        f = request.files['file']
        if f and allowed_file(f.filename):
            filename = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER']), filename)
    return jsonify(code=1)


#######################################
# 定制错误页面
@app.errorhandler(401)
def page_not_found(error):
    return render_template('401.html'), 404
#######################################

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

