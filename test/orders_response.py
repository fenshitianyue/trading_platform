#!/usr/bin/python2
# coding:utf-8

response = []

num = 0
for i in range(len("abcde")):
    dict = {}
    dict['title'] = "test title"
    dict['doc'] = "test doc"
    response.append(dict)
    num = num + 1

print response
