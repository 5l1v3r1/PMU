#!/usr/bin/python
# Startup script for the clients to connect with the remote server.

import sys, os, socket, select, time, datetime, getpass

#if (len(sys.argv) < 3):
#    print("Usage: python connector.py <host> <port>")
#    sys.exit(0)

#host = ''
#port = 3435

host = raw_input('IP \> ')
port = input('Port \> ')
_key = raw_input('Key \> ')

def connector():
    server = socket.socket(socket.AF_INET)
    server.settimeout(1)

    try:
        server.connect((host, port))
        print("Connected to %s on port %s" % (host, port))
        print("Listening...\n")
        server.send('USER$' + getpass.getuser() + '$KEY$' + _key)
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
                    os.system(data.split('$')[1])
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


try:
    connector()
except KeyboardInterrupt:
    print("\033[1;91m[!]\033[0m Disconnected")
