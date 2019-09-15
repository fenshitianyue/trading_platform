#!/usr/bin/python2
# coding:UTF-8

from datetime import datetime

tmp = datetime.now()

# print tmp
# print type(tmp)
#
now_time = str(tmp)
#
# print now_time
# print type(now_time)

now_time = now_time[0:-7]
print now_time
print type(now_time)
