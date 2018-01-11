#!/usr/bin/python
# Server script
# From here, the controller will get connected clients.
# Write online clients to text file
# Print format:
#   On/Offline     Key          Hostname         User              IP      Package Status
#   If data       KEY$       gethostbyname()  getpass.getuser()    addr          ??

import sys, socket, select, os

host = ''
port = 3435
#port = int(sys.argv[1])

socket_list = []

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
                else:
                    try:
                        data = sock.recv(4096)
                        if data:
                            if not 'USER' in data:
                                broadcast(server_socket, sock, ' ' + data)
                                print("[ " + str(sock.getpeername()[0]) + " ] " + data)

                            if '$' in data:
                                print(data.split('$')[1])
                                if data.split('$')[0] == 'USER':
                                    _user = data.split('$')[1]
                                    _key = data.split('$')[3]
                                    print('\33[1;92m[Online]\033[0m' + _key.rjust(10) + socket.gethostbyaddr(addr[0])[0].rjust(15) + _user.rjust(15) + addr[0].rjust(15) + 'PACKAGE STATUS'.rjust(20))
                        else:
                            # If there is no data, remove it from the list
                            if sock in socket_list:
                                socket_list.remove(sock)

                            #broadcast(server_socket, sock, "Connection with [%s:%s] interrupted" % addr)
                            print('\33[1;91m[Offline]\033[0m' + _key.rjust(10) + socket.gethostbyaddr(addr[0])[0].rjust(15) + _user.rjust(15) + addr[0].rjust(15) + 'PACKAGE STATUS'.rjust(20))
                            #print("[-] %s:%s Disconnected" % addr)

                    except Exception as e:
                        broadcast(server_socket, sock, "Connection with [%s:%s] interrupted" % addr)
                        continue
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print('\nServer closed...')

    server_socket.close()

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

if __name__ == "__main__":
    sys.exit(main_controller())
