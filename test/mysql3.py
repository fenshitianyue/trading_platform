#!/usr/bin/python2
#coding=UTF-8

import MySQLdb

username = "zero123"
new_passwd = "passwd123"
# new_passwd = "test123"

db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset="utf8")
cursor = db.cursor()
sql = "update dev set dev_passwd = '" + new_passwd + "'" + " where dev_username = '" + username + "'"

cursor.execute(sql)
db.commit()

sql = "select dev_passwd from dev where dev_username = '" + username + "'"
cursor.execute(sql)
result = cursor.fetchone()

dev_passwd = result[0]

if dev_passwd == new_passwd:
    print "修改成功"
else:
    print "修改失败"

db.close()

