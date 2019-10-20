#!/usr/bin/python
# -*- coding:UTF-8 -*-

def get_string(status):
    if 1 == status:
        return "string 1"
    elif 2 == status:
        return "string 2"
    else:
        raise Exception("none faild!")

def func_top():
    try:
        string = get_string(3)
    except Exception, err:
        print err
        return
    print string

if __name__ == '__main__':
    func_top()
