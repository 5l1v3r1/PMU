#!/usr/bin/python
# Startup script for the clients to connect with the remote server.

import sys, os, socket, select, time, datetime, getpass, base64, subprocess
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

BS = 256
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

    def decrypt(self, enc ):
        enc = base64.b64decode(enc)
        iv = enc[:16]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return unpad(cipher.decrypt( enc[16:]))

# AES secret
cipher = AESCipher('<\x18\xadx\xbfp2\xf6\x9aH\xa3\xd3q}D\xe9\xce\\\xdf\x05XS\x7f\xce*m]5\xde\xcd\xf2\xa6') # Key

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

        # Get package status
        p = subprocess.Popen("sudo apt-get -u upgrade --assume-no | grep upgraded,", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()

        #print(output.split('upgrade')[0]) # Debug

        server.send(cipher.encrypt('USER$' + getpass.getuser() + '$KEY$' + _key + '$STATUS$' + output.split('upgrade')[0]))

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
                    data = sock.recv(2048)

                    # Try to decrypt data
                    try:
                        data = cipher.decrypt(data)
                    except Exception as e:
                        print(data) # Debug
                        print(e)
                        print('\033[1;91m[ERROR]\033[0m Failed to execute command %s' % data)

                if not data:
                    print("\033[1;91m[!]\033[0m Connection has ended")
                    sys.exit(1)
                else:
                    print(data) # Debug

                # Do something when some data is present
                if 'COMMAND$' in data:
                    # Run command
                    if not data.split('$')[1].startswith('rm'):
                        os.system(data.split('$')[1])
                    else:
                        print('\033[1;94m[ INFO ]\033[0m Commanded Blocked: %s' % data.split('$')[1])

                elif 'SHUTDOWN$' in data:
                    if data.split('$')[1] == _key:
                        os.system('poweroff')
                    # Check Key > if my Key >> do, if 'all' >> do
                elif 'REBOOT$' in data:
                    if data.split('$')[1] == _key:
                        os.system('reboot')
                elif 'UPGRADE$' in data:
                    if data.split('$')[1] == _key and getpass.getuser() == 'root':
                        try:
                            os.system('apt-get update && apt-get upgrade -y')
                        except Exception as e:
                            print('[ERROR] Failed to update')
    except Exception as e:
        print(e)

# Starts script
try:
    connector()
except KeyboardInterrupt:
    print("\033[1;91m[!]\033[0m Disconnected")
