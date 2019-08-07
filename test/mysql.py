#!/usr/bin/python2
# coding:utf-8

import MySQLdb


db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset='utf8')

cursor = db.cursor()

username = 'test123'

sql = "select dev_name from dev where dev_name = '" + username + "'"

cursor.execute(sql)

result = cursor.fetchall()

if result:
    print "该用户名已存在! Raw: " + username
else:
    print "该用户名可用!"
