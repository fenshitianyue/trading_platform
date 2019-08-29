#!/usr/bin/python2
# coding:utf-8

tmp = [4000]

num_set = tuple(tmp)

sql = "select * from orders where order_num in " + str(num_set)
print sql
sql = sql[0:-2]
sql = sql + ")"
print sql
