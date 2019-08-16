#!/usr/bin/python2
#coding=UTF-8

import MySQLdb

username = "zero123"
passwd = "passwd123"

db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset="utf8")
cursor = db.cursor()
sql = "select dev_username, dev_passwd from dev where dev_username = '" + username + "'"

cursor.execute(sql)
result = cursor.fetchone()

if not result:
    print "用户名不存在"
else:
    # dev_username = result[0]
    dev_passwd = result[1]
    if dev_passwd == passwd:
        print "登陆成功"
    else:
        print "密码错误"


