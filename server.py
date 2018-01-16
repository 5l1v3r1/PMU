#!/usr/bin/python
# Server script
# From here, the controller will get connected clients.
# Write online clients to text file
# Print format:
#   On/Offline     Key          Hostname         User              IP      Package Status
#   If data       KEY$       gethostbyname()  getpass.getuser()    addr          ??
import sys, socket, select, os, base64
from Crypto import Random
from Crypto.Cipher import AES

#if (len(sys.argv) < 2):
#    print("Usage: python main_controller.py <port>")
#    sys.exit(0)


# Vars
host = ''
port = 3435

_logfile = './logfile.log'
_userslog = './users.csv'

#port = int(sys.argv[1])

socket_list = []

BS = 256
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
unpad = lambda s : s[0:-ord(s[-1])]

class AESCipher:
    def __init__(self, key ):
        self.key = key

    def encrypt(self, raw ):
        raw = pad(raw)
        iv = Random.new().read(AES.block_size)
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

# Server script
def main_controller():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(10)

    socket_list.append(server_socket)

    print("\033[1;92m[ OK ]\033[0m Listening on port %s" % port)

    try:
        while True:
            ready_read,ready_write,in_error = select.select(socket_list,[],[],0)

            for sock in ready_read:
                if sock == server_socket:
                    sockfd, addr = server_socket.accept()
                    socket_list.append(sockfd)

                    #Send broadcast to let clients know a new client connected
                    #broadcast(server_socket, sock, "\r" + "[%s:%s] Connected" % addr)

                else:
                    try:
                        data = sock.recv(2048)

                        # Try to decrypt the data, else, show plain data
                        try:
                            data = cipher.decrypt(data)
                        except Exception as e:
                            print('Plain data:')
                            print(data)
                            print('----------------------------')

                        if data:
                            if not 'USER' in data:
                                broadcast(server_socket, sock, ' ' + cipher.encrypt(data))
                                print("[ " + str(sock.getpeername()[0]) + " ] " + data)

                                with open(_logfile, 'a+') as f:
                                    f.write("[ " + str(sock.getpeername()[0]) + " ] " + data + '\n')
                                    f.close()

                            if '$' in data:
                                #print(data.split('$')[1]) # Debug

                                if data.split('$')[0] == 'USER':
                                    _user = data.split('$')[1] # Grab user
                                    _key = data.split('$')[3] # Grab Key
                                    _upgrades = data.split('$')[5] + 'Upgrades' # Grab upgrades

                                    #print(data)

                                    print('\33[1;92m[Online]\033[0m %s for %s (%s) | User: %s' % (_upgrades, addr[0], _key, _user)) # Debug
                                    with open(_userslog, 'a+') as f:
                                        f.write('[Online] %s for %s (%s) | User: %s\n' % (_upgrades, addr[0], _key, _user))
                                        f.close()

                                    # Read Available keys
                                    try:
                                        _keylist = open('keys-available.csv').read()
                                        #print(_keylist) # Debug
                                    except Exception as e:
                                        _keylist = ''

                                    if _key in _keylist:

                                        _keylist = _keylist.replace(_key, '%s,%s,%s' % (_key, addr[0], addr[1]))

                                        #print('\33[1;92m[Online]\033[0m' + _key.rjust(10) + socket.gethostbyaddr(addr[0])[0].rjust(15) + _user.rjust(15) + addr[0].rjust(15) + _upgrades.rjust(20))

                                        # Replace line in keylist
                                        with open('keys-available.csv', 'w') as f:
                                            f.writelines(_keylist); f.close()

                                    else:
                                        # Invalid key, remove client socket
                                        print('\033[1;91m[ERROR]\033[0m Invalid key entrered from %s (kicked from the server)' % addr[0])
                                        if sock in socket_list:
                                            socket_list.remove(sock)
                                        
                                elif data.split('$')[1] == 'online':
                                    for l in open(_userslog, 'r').readlines():
                                        if l.startswith('[Online]'):
                                            _online = l.rstrip() + '\n'
                                            broadcast(server_socket, sock, cipher.encrypt(_online))

                                elif data.split('$')[0] == 'KEY':
                                    with open('keys-available.csv', 'a+') as f:
                                        f.write(data.split('$')[1] + '\n'); f.close()
                        else:
                            # If there is no data, remove it from the list
                            if sock in socket_list:
                                socket_list.remove(sock)

                            _online_status = open(_userslog).readlines()

                            # Replace line [Online] with [Offline]
                            # *Do Magic*

                            #broadcast(server_socket, sock, "Connection with [%s:%s] interrupted" % addr)
                            print('\33[1;91m[Offline]\033[0m ' + addr[0])
                            #print("[-] %s:%s Disconnected" % addr)

                    except Exception as e:
                        broadcast(server_socket, sock, cipher.encrypt("Connection with [%s:%s] interrupted" % addr))
                        continue
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('\nServer closed...')

    server_socket.close()

# Broadcast to all clients
def broadcast (server_socket, sock, msg):
    for socket in socket_list:
        # send the message only to peer
        if socket != server_socket and socket != sock:
            try:
                socket.send(msg)
            except:
                # broken socket connection
                socket.close()
                # broken socket, remove it
                if socket in socket_list:
                    socket_list.remove(socket)

# Starts script
if __name__ == "__main__":
    sys.exit(main_controller())
