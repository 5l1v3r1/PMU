#!/usr/bin/python
# Startup script for the clients to connect with the remote server.

import sys, os, socket, select, time, datetime, getpass, base64
from Crypto import Random
from Crypto.Cipher import AES

#if (len(sys.argv) < 3):
#    print("Usage: python connector.py <host> <port>")
#    sys.exit(0)

# Vars
host = ''
port = 3435

#host = raw_input('IP \> ')
#port = input('Port \> ')
_key = raw_input('Authentication Key \> ')

BS = 128
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

# AES Encryption
class AESCipher:
    def __init__(self, key ):
        self.key = key

    def encrypt(self, raw ):
        raw = pad(raw)
        iv = Random.new().read( AES.block_size )
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

# AES secret
cipher = AESCipher('LK0315B4NNKOX1JMR2P0NL188KXJXFUT') # 32 character password

# SSL Encryption
#*Do magic*

# Connect to remote server
def connector():
    server = socket.socket(socket.AF_INET)
    server.settimeout(1)

    try:
        server.connect((host, port))
        print("Connected to %s on port %s" % (host, port))
        print("Listening...\n")
        #print(cipher.encrypt(_key)) # Debug
        server.send('USER$' + getpass.getuser() + '$KEY$' + cipher.encrypt(_key))
    except Exception as e:
        print("\033[1;91m[ ! ]\033[0m Unable to connect to %s on port %s" % (host, port))
        print(e)
        sys.exit(1)

    try:
        while True:
            socket_list = [sys.stdin, server]
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

            for sock in read_sockets:
                if sock == server:
                    data = sock.recv(4096)
                if not data:
                    print("\033[1;91m[!]\033[0m Connection has ended")
                    sys.exit(0)
                else:
                    print("\033[1;94m[ INFO ]\033[0m %s" % data)

                # Do something when some data is present
                if 'COMMAND$' in data:
                    # Run command
                    if not data.split('$')[1].startswith('rm'):
                        os.system(data.split('$')[1])
                    else:
                        print('\033[1;94m[ INFO ]\033[0m Commanded Blocked: %s' % data.split('$')[1])
                elif 'SHUTDOWN$' in data:
                    print(data.split('$')[1])
                    # Check IP > if my IP >> do, if 'all' >> do
                elif 'REBOOT$' in data:
                    print(data.split('$')[1])
                    # Check IP > if my IP >> do, if 'all' >> do
                elif 'UPGRADE$' in data:
                    print(data.split('$')[1])
                    # Check IP > if my IP >> do, if 'all' >> do
    except Exception as e:
        print(e)

# Starts script
try:
    connector()
except KeyboardInterrupt:
    print("\033[1;91m[!]\033[0m Disconnected")
