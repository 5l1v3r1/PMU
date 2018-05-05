#!/usr/bin/python
import os, sys, socket, time, threading, random, string, base64, select
from Crypto import Random
from Crypto.Cipher import AES
from Tkinter import *
from ttk import *

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

global cipher
cipher = AESCipher('<\x18\xadx\xbfp2\xf6\x9aH\xa3\xd3q}D\xe9\xce\\\xdf\x05XS\x7f\xce*m]5\xde\xcd\xf2\xa6')

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = '<< Remote Administration Tool | Dashboard >>')
        self.resizable(0,0)
        self.style = Style()
        self.style.theme_use("clam")

        self.options = {
            'server' : StringVar(),
            'port' : IntVar(),
            'command' : StringVar(),
            'key' : StringVar(),
            'shellbar' : StringVar(),

        }

        # Set default options
        self.options['server'].set('127.0.0.1')
        self.options['port'].set(3435)

        global s
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(2)

        # Start time thread
        time_thread = threading.Thread(target=self.date_time)
        time_thread.daemon = True
        time_thread.start()

        settings = LabelFrame(self, text = 'Client Settings')
        settings.grid(row = 0, column = 1)

        Label(settings, text = 'Server').grid(row = 0, column = 1)
        Entry(settings, textvariable = self.options['server'], width = 30).grid(row = 0, column = 2)

        Label(settings, text = 'Port').grid(row = 1, column = 1)
        Entry(settings, textvariable = self.options['port'], width = 30).grid(row = 1, column = 2)
        connect_button = Button(settings, text = 'Connect', command = self.connect, width = 20).grid(row = 0, column = 3, rowspan = 2)

        Label(settings, text = 'Key').grid(row = 2, column = 1)
        Entry(settings, textvariable = self.options['key'], width = 30).grid(row = 2, column = 2)
        generate_key = Button(settings, text = 'Generate Key', command = self.create_key, width = 20).grid(row = 2, column = 3)

        Label(settings, text = 'Key').grid(row = 3, column = 1)
        Entry(settings, textvariable = self.options['key'], width = 30).grid(row = 3, column = 2)
        generate_key = Button(settings, text = 'Delete Key', command = '', width = 20).grid(row = 3, column = 3)

        Label(settings, text = 'Key').grid(row = 4, column = 1)
        Entry(settings, textvariable = self.options['key'], width = 30).grid(row = 4, column = 2)
        generate_key = Button(settings, text = 'Check key', command = '', width = 20).grid(row = 4, column = 3)


        features = LabelFrame(self, text = 'Features')
        features.grid(row = 0, column = 2)

        Label(features, text = 'Execute command').grid(row = 0, column = 1)
        self.options['command'] = Entry(features, textvariable = self.options['command'], width = 50)
        self.options['command'].grid(row = 0, column = 2, columnspan = 3)
        execute_button = Button(features, text = 'Execute', command = self.send_command, width = 20).grid(row = 0, column = 5)

        clear_log = Button(features, text = 'Clear log', command = self.clear_log, width = 20).grid(row = 1, column = 1)
        save_log = Button(features, text = 'Save log', command = '', width = 20).grid(row = 2, column = 1)
        save_log = Button(features, text = 'List Available Keys', command = '', width = 20).grid(row = 3, column = 1)

        shutdown_button = Button(features, text = 'Refresh client list', command = '', width = 20).grid(row = 1, column = 3)
        drop_shell = Button(features, text = 'Drop to Shell', command = self.drop_to_shell, width = 20).grid(row = 2, column = 3)

        update_all = Button(features, text = 'Update All Clients', command = self.update_all, width = 20).grid(row = 1, column = 4)
        update = Button(features, text = 'Update Selected Client', command = self.update_client, width = 20).grid(row = 2, column = 4)

        shutdown_all_button = Button(features, text = 'Shutdown All Client', command = self.shutdown_all, width = 20).grid(row = 1, column = 5)
        shutdown_button = Button(features, text = 'Shutdown Selected Client', command = self.shutdown_client, width = 20).grid(row = 2, column = 5)

        reboot_all = Button(features, text = 'Reboot All Client', command = self.reboot_all, width = 20).grid(row = 3, column = 5)
        reboot = Button(features, text = 'Reboot Selected Client', command = self.reboot_client, width = 20).grid(row = 4, column = 5)

        server = LabelFrame(self, text = 'Server')
        server.grid(row = 0, column = 3)

        start_server_button = Button(server, text = 'Start Server', width = 20).grid(row = 0, column = 1)
        stop_server_button = Button(server, text = 'Stop Server', width = 20).grid(row = 1, column = 1)
        restart_server_button = Button(server, text = 'Restart Server', width = 20).grid(row = 2, column = 1)

        client_frame = LabelFrame(self, text = 'Clients Area', height = 400, width = 1400)
        client_frame.grid(row = 1, column = 1, columnspan = 3)

        Label(client_frame, text = 'Client list').grid(row = 0, column = 1)
        self.options['clients'] = Listbox(client_frame, width = 120, height = 30)
        self.options['clients'].grid(row = 1, column = 1)
        self.options['clients'].bind("<Double-Button-1>", self.drop_to_shell)

        # Log Frame
        Label(client_frame, text = 'Log').grid(row = 0, column = 2)
        self.options['log'] = Text(client_frame, foreground = 'white', background = 'black', height = 32)
        self.options['log'].grid(row = 1, column = 2)

        # Tags
        self.options['log'].tag_configure('yellow', foreground='yellow') # Common Message
        self.options['log'].tag_configure('red', foreground='red') # Error
        self.options['log'].tag_configure('deeppink', foreground='deeppink') # Special
        self.options['log'].tag_configure('orange', foreground='orange') # Danger
        self.options['log'].tag_configure('green', foreground='green') # Ok
        self.options['log'].tag_configure('bold', font='bold')

    def connect(self):
        try:
            s.connect((self.options['server'].get(), self.options['port'].get()))

            # Start time thread
            server_thread = threading.Thread(target=self.keep_alive)
            server_thread.daemon = True
            server_thread.start()

            self.options['log'].insert('1.0', '[%s %s] Connected to <%s:%s>\n' % (time.strftime('%x'), time.strftime('%X'), self.options['server'].get(), self.options['port'].get()), 'green')
        except Exception as e:
            self.options['log'].insert('1.0', '[ERROR] Failed to connect: %s\n' % e, 'red')

    def keep_alive(self):
        running = True
        while running:
            socket_list = [sys.stdin, s]

            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = select.select(socket_list , [], [])

            for sock in read_sockets:
                if sock == s:
                    data = sock.recv(2048)
                    data = cipher.decrypt(data)
                    if not data:
                        self.options['log'].insert('1.0', '[%s %s] Disconnected from server\n' % (time.strftime('%x'), time.strftime('%X')), 'red')
                        sys.exit(1)
                    else:
                        # print data
                        if data.startswith('[Online]'):
                            # If already in list, ignore, else, append.
                            if not data in self.options['clients'].get(0, END):
                                self.options['clients'].insert(END, data)

                        else:
                            self.options['log'].insert('1.0', '%s\n' % data, 'yellow')
                            try:
                                self.options['shellframe'].insert('1.0', '%s\n' % data, 'yellow')
                            except Exception:
                                pass

    def drop_to_shell(self, event):
        try:
            selection = self.options['clients'].get(self.options['clients'].curselection())
        except Exception:
            self.options['log'].insert('1.0', '[%s %s] [ERROR] Please, select a client' % (time.strftime('%x'), time.strftime('%X')), 'red')

        selection = self.options['clients'].get(self.options['clients'].curselection())
        self.options['key'] = selection.split('(')[1].split(')')[0]

        ip = self.options['clients'].get(self.options['clients'].curselection())
        ip = selection.split(' ')[4]

        self.shell = Toplevel()
        self.shell.title(string = 'Shell access for %s [%s]' % (ip, self.options['key']))
        self.shell.resizable(0,0)

        # Command output frame
        self.options['shellframe'] = Text(self.shell, background = 'black', foreground = 'white', height = 32, width = 80)
        self.options['shellframe'].grid(row = 0, column = 1)

        # Command input entry
        self.options['shellbar'] = Entry(self.shell, textvariable = self.options['shellbar'], width = 70)
        self.options['shellbar'].grid(row = 2, column = 1)
        self.options['shellbar'].bind('<Return>', self.send_command_client)
        self.options['shellbar'].focus()


    def send_command_client(self, event):
        self.options['shellframe'].insert('1.0', self.options['shellbar'].get() + '\n')
        s.send(cipher.encrypt('YOUDO$' + self.options['key'] + '$' + self.options['shellbar'].get()))
        self.options['shellbar'].delete(0, END) # Clear shellbar

    def send_command(self):
        s.send(cipher.encrypt('COMMAND$' + self.options['command'].get()))
        self.options['log'].insert('1.0', '[%s %s] Executed command on all clients: %s\n' % (time.strftime('%x'), time.strftime('%X'), self.options['command'].get()), 'yellow')
        self.options['command'].delete(0, END)

    def update_client(self):
        selection = self.options['clients'].get(self.options['clients'].curselection())
        selection = selection.split('(')[1].split(')')[0] # Grab key
        s.send(cipher.encrypt('UPGRADE$' + selection)) # Send update command
        self.options['log'].insert('1.0', '[%s %s] Updated %s' % (time.strftime('%x'), time.strftime('%X'), selection), 'yellow')

    def update_all(self):
        s.send(cipher.encrypt('COMMAND$apt-get update && apt-get upgrade -y'))
        self.options['log'].insert('1.0', '[%s %s] Updated all client\n' % (time.strftime('%x'), time.strftime('%X')), 'yellow')

    def clear_log(self):
        self.options['log'].delete('1.0', END)

    def shutdown_client(self):
        selection = self.options['clients'].get(self.options['clients'].curselection())
        selection = selection.split('(')[1].split(')')[0] # Grab key
        s.send(cipher.encrypt('SHUTDOWN$' + selection)) # Send poweroff command
        self.options['log'].insert('1.0', '[%s %s] Updated %s' % (time.strftime('%x'), time.strftime('%X'), selection), 'yellow')

    def shutdown_all(self):
        s.send(cipher.encrypt('COMMAND$poweroff'))
        self.options['log'].insert('1.0', '[%s %s] Shutdown all client\n' % (time.strftime('%x'), time.strftime('%X')), 'yellow')

    def reboot_client(self):
        selection = self.options['clients'].get(self.options['clients'].curselection())
        selection = selection.split('(')[1].split(')')[0] # Grab key
        s.send(cipher.encrypt('REBOOT$' + selection)) # Send reboot command
        self.options['log'].insert('1.0', '[%s %s] Rebooted %s' % (time.strftime('%x'), time.strftime('%X'), selection), 'yellow')

    def reboot_all(self):
        s.send(cipher.encrypt('COMMAND$reboot'))
        self.options['log'].insert('1.0', '[%s %s] Rebooted all client\n' % (time.strftime('%x'), time.strftime('%X')), 'yellow')

    def create_key(self):
        key = gen_string()
        self.options['key'].set(key)
        s.send(cipher.encrypt('KEY$' + key))
        self.options['log'].insert('1.0', '[%s %s] A new key was added: %s\n' % (time.strftime('%x'), time.strftime('%X'), key), 'yellow')


    def date_time(self):
        while True:
            self.title(string = '<< Remote Administration Tool | Dashboard | %s %s >>' % (time.strftime('%x'), time.strftime('%X')))
            time.sleep(1)

# Generate Key
def gen_string(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    try:
        panel = MainWindow()
        panel = mainloop()
    except Exception as e:
        print('[ERROR] %s' % e)
