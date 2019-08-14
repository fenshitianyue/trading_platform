#!/usr/bin/python2
# coding : utf-8

import random

def gen():
    ic = ""
    for i in range(6):
        c = chr(random.randrange(65, 91))
        ic = ic + c
    print ic
    print "----"
    return ic

if __name__ == '__main__':
    ss = gen()
    print ss
