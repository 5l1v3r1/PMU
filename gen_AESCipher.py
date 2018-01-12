#!/usr/bin/python
import sys, os, random, string, hashlib

length = 32

def gen_string(size=length, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

passwd = gen_string(); print('%s\n\n') % passwd

key = hashlib.sha256(passwd).digest(); print('Encrypted:\n\n'); print('',key)
