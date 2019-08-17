#!/usr/bin/python2
#coding=UTF-8

import base64
import gvcode
from cStringIO import StringIO

# size=(60, 27),
img, code = gvcode.generate(size=(80, 27), length=4)  # code:验证码的值

out = StringIO()
img.save(out, format='PNG')
b64 = base64.b64encode(out.getvalue())

result = "data:image/png;base64,"
result = result + b64
# print result, code
print code
img.save('./captcha.png')




