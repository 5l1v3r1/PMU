#!/usr/bin/python3
import sys, os, random, string, hashlib

if (len(sys.argv) < 2):
    print('[!] Usage: python gen_passwd.py <passwd length>')
    sys.exit()

length = int(sys.argv[1])

def gen_string(size=length, chars=string.ascii_uppercase + string.digits):
      return ''.join(random.choice(chars) for _ in range(size))

passwd = gen_string(); print('%s\n\n') % passwd

key = hashlib.sha256(passwd).digest(); print('Encrypted:\n\n'); print('',key)
