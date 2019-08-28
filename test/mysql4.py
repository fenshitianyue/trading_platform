#!/usr/bin/python2
# coding:utf-8

import MySQLdb

pageNumber = 1
pageSize = 10
path_pre = "/document"
db = MySQLdb.connect("localhost", "root", "nihao.", "itkim", charset="utf8")
cursor = db.cursor()
sql = "select * from orders limit " + str((pageNumber-1)*pageSize) + "," + str(pageSize)

cursor.execute(sql)
# result = cursor.fetchall()
row = cursor.fetchone()

# response = []
# for row in result:
#     dict = {}
#     dict['id'] = row[0]
#     dict['title'] = row[1]
#     dict['publishTime'] = row[2]
#     dict['dueTime'] = row[3]
#     dict['orderTag'] = row[4]
#     dict['requireType'] = row[5]
#     dict['devPrice'] = row[6]
#     dict['docFilePath'] = path_pre + row[7]
#     dict['allFilePath'] = path_pre + row[8]
#     dict['requirement'] = row[9]
#     dict['devRemark'] = row[10]
#     dict['orderStatus'] = row[11]
#     dict['pickFlag'] = row[12]
#     response.append(dict)

dict = {}
dict['id'] = row[0]
dict['title'] = row[1]
dict['publishTime'] = row[2]
dict['dueTime'] = row[3]
dict['orderTag'] = row[4]
dict['requireType'] = row[5]
dict['devPrice'] = row[6]
dict['docFilePath'] = path_pre + row[7]
dict['allFilePath'] = path_pre + row[8]
dict['requirement'] = row[9]
dict['devRemark'] = row[10]
dict['orderStatus'] = row[11]
dict['pickFlag'] = row[12]

# print response
print dict['publishTime']
print type(dict['publishTime'])
publishTime = str(dict['publishTime'])
print publishTime
print type(publishTime)

db.close()
