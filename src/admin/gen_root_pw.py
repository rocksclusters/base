#!@PYTHON@

import os
import sys
import base64
import crypt

def get_pw():
	salt = '$1$'
	f = open('/dev/urandom','r')
	s = f.read(16)
	salt = salt + base64.b64encode(s,'./')[0:8]
	s = base64.b64encode(f.read(16), './')
	f.close()
	return crypt.crypt(s, salt)

if __name__ == '__main__':
	print get_pw()
