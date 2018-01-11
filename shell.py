#!/usr/bin/python
# Connects with the server and send commands.
# This will be the command shell

import sys, socket, select, os, string, random

halp = '''
Help:
    \033[1;95mCommand\033[0m\t\t\t| \033[1;95mDescription\033[0m
    /help\t\t\t| Show this help
    clear\t\t\t| Clear terminal screen
    /genkey\t\t\t| Generate token to connect
    /del <key>\t\t\t| Delete key for host
    /update <IP>\t\t| Update remote client
    /update all\t\t\t| Update all remote clients
    /connect <IP>\t\t| Reverse shell on remote client
    /c <command>\t\t| Send command to all clients
    /shutdown <IP>\t\t| Shutdown remote client
    /shutdown all\t\t| Shutdown all remote clients
    /reboot <IP>\t\t| Reboot remote client
    /reboot all\t\t\t| Reboot all remote clients
    /show list\t\t\t| Show all clients
    /show online\t\t| Show all Online clients
    /show offline\t\t| Show all Offine clients
    exit\t\t\t| Terminate the service
'''

def gen_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def chat_client():
    #if(len(sys.argv) < 3) :
    #    print 'Usage : python chat-client.py <server> <port>'
    #    sys.exit(0)

    host = ''
    port = 3435
    #host = sys.argv[1]
    #port = int(sys.argv[2])

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
                    # incoming message from remote server, s
                    data = sock.recv(4096)
                    if not data:
                        print '\nDisconnected from server'
                        sys.exit(1)
                    else:
                        # print data
                        sys.stdout.write(data)
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
                            s.send('COMMAND$apt-get update && apt-get upgrade -y')
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                        else:
                            s.send('UPGRADE$' + msg.split(' ')[1])
                            sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/save'):
                        print('\nComming Soon...\n')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/connect'):
                        print('\nComming Soon...\n')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/c'):
                        msg = msg.replace('/c ', '')
                        s.send('COMMAND$' + msg.rstrip())
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/shutdown '):
                        s.send('COMMAND$poweroff')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/shutdown all'):
                        s.send('COMMAND$poweroff')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/reboot '):
                        print('\nComming Soon...\n')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/reboot all'):
                        s.send('COMMAND$reboot')
                        sys.stdout.write('#?\PMU\> '); sys.stdout.flush()
                    elif msg.startswith('/show'):
                        print('\nComming Soon...\n')
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
    sys.exit(chat_client())
