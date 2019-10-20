#!/usr/bin/python2
# -*- coding:UTF-8 -*-

def get_string(status):
    if 1 == status:
        return "string 1"
    elif 2 == status:
        return "string 2"
    else:
        raise Exception("none faild: ", "argv[0]", "argv[1]")

def func_top():
    try:
        string = get_string(3)
    except Exception, err:
        print err[0] + err[1] + "," + err[2]
        return
    print string

# def test_file():
#     try:
#         fd = open("testfile", "w")
#         try:
#             fd.write("this is a test file, useing to test abnormal!!!")
#         finally:
#             print "close file!"
#             fd.close()
#     except IOError:
#         print "Error: file not found or read file faild!"

if __name__ == '__main__':
    func_top()
    # test_file()
