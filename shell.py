#!/usr/bin/python
# Connects with the server and send commands.
# This will be the command shell

import sys, socket, select, os, string, random, base64
from Crypto import Random
from Crypto.Cipher import AES

halp = '''
Help:
    \033[1;95mCommand\033[0m\t\t\t| \033[1;95mDescription\033[0m
    /help\t\t\t| Show this help
    clear\t\t\t| Clear terminal screen
    /genkey\t\t\t| Generate token to connect
    /del <key>\t\t\t| Delete key for host
    /update <key>\t\t| Update remote client
    /update all\t\t\t| Update all remote clients
    /connect <key>\t\t| Reverse shell on remote client
    /c <command>\t\t| Send command to all clients
    /shutdown <key>\t\t| Shutdown remote client
    /shutdown all\t\t| Shutdown all remote clients
    /reboot <key>\t\t| Reboot remote client
    /reboot all\t\t\t| Reboot all remote clients
    /show list\t\t\t| Show all clients
    /show online\t\t| Show all Online clients
    /show offline\t\t| Show all Offine clients
    exit\t\t\t| Terminate the service
'''

def gen_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

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

# AES secret
cipher = AESCipher('<\x18\xadx\xbfp2\xf6\x9aH\xa3\xd3q}D\xe9\xce\\\xdf\x05XS\x7f\xce*m]5\xde\xcd\xf2\xa6') # Key

def client():
    #if(len(sys.argv) < 3) :
    #    print 'Usage : python chat-client.py <server> <port>'
    #    sys.exit(0)

    host = ''
    port = 3435

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)

    # connect to host
    try:
        s.connect((host, port))
    except:
        print '[ ERROR ] Unable to connect'
        sys.exit(1)
    os.system('clear')
    print '\n\t\t[ WELCOME ] Connected with ' + str(host) + ':' + str(port) + '\n\n'
    sys.stdout.write('#?\PMU\> '); sys.stdout.flush()

    try:
        while 1:
            socket_list = [sys.stdin, s]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

            for sock in read_sockets:
                if sock == s:
                    data = sock.recv(2048)
                    if not data:
                        print '\nDisconnected from server'
                        sys.exit(1)
                    else:
                        # print data
                        print('%s' % data)
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                else:
                    # user entered a message
                    msg = sys.stdin.readline()

                    if msg.startswith('?'):
                        print(halp)
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/help'):
                        print(halp)
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('exit'):
                        print('Exiting...'); sys.exit(0)
                    elif msg.startswith('clear'):
                        os.system('clear')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/genkey'):
                        print('New key added: ' + gen_string())
                        #print('\nComming Soon...\n')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/del'):
                        print('\nComming Soon...\n')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/update '):
                        msg = msg.rstrip()
                        if 'all' in msg.split(' ')[1]:
                            #s.send('COMMAND$apt-get update && apt-get upgrade -y')
                            s.send(cipher.encrypt('COMMAND$apt-get update && apt-get upgrade -y'))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        else:
                            s.send(cipher.encrypt('UPGRADE$' + msg.split(' ')[1]))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/save'):
                        print('\nComming Soon...\n')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/connect'):
                        print('\nComming Soon...\n')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/c'):
                        msg = msg.replace('/c ', '').rstrip()
                        s.send(cipher.encrypt('COMMAND$' + msg))
                        #s.send('COMMAND$' + msg)
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/shutdown '):
                        s.send(cipher.encrypt('COMMAND$poweroff'))
                        #s.send('COMMAND$poweroff')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/shutdown '):
                        if 'all' in msg.split(' ')[1]:
                            #s.send('COMMAND$apt-get update && apt-get upgrade -y')
                            s.send(cipher.encrypt('COMMAND$poweroff'))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        else:
                            s.send(cipher.encrypt('SHUTDOWN$' + msg.split(' ')[1]))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        #s.send('COMMAND$poweroff')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/reboot '):
                        if 'all' in msg.split(' ')[1]:
                            #s.send('COMMAND$apt-get update && apt-get upgrade -y')
                            s.send(cipher.encrypt('COMMAND$reboot'))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        else:
                            s.send(cipher.encrypt('REBOOT$' + msg.split(' ')[1]))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        #s.send('COMMAND$reboot')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/show'):
                        if 'online' in msg.split(' ')[1]:
                            #s.send('SHOW$online')
                            s.send(cipher.encrypt('SHOW$online'))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        elif 'offline' in msg.split(' ')[1]:
                            #s.send('SHOW$offline')
                            s.send(cipher.encrypt('SHOW$offline'))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        elif 'list' in msg.split(' ')[1]:
                            s.send('SHOW$list')
                            s.send(cipher.encrypt('SHOW$list'))
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        else:
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    else:
                        if msg.startswith('/'):
                            s.send(msg)
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        else:
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('\nExiting...'); sys.exit(0)

if __name__ == "__main__":
    sys.exit(client())
