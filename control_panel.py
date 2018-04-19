#!/usr/bin/python
import os, sys, socket, time, threading, random, string, base64
from Crypto import Random
from Crypto.Cipher import AES
from Tkinter import *

class MainWindow(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title(string = '<< Remote Administration Tool | Control Panel >>')
        self.resizable(0,0)
        #self.geometry('1250x600')

        self.options = {
            'server' : StringVar(),
            'port' : IntVar(),
            'command' : StringVar(),
            'key' : StringVar(),

        }

        # Set default options
        self.options['server'].set('127.0.0.1')
        self.options['port'].set(8989)

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
        connect_button = Button(settings, text = 'Connect', command = '', width = 20, height = 2).grid(row = 0, column = 3, rowspan = 2)

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
        Entry(features, textvariable = self.options['command'], width = 50).grid(row = 0, column = 2, columnspan = 3)
        execute_button = Button(features, text = 'Execute', command = '', width = 20).grid(row = 0, column = 5)

        clear_log = Button(features, text = 'Clear log', command = '', width = 20).grid(row = 1, column = 1)
        save_log = Button(features, text = 'Save log', command = '', width = 20).grid(row = 2, column = 1)
        save_log = Button(features, text = 'List Available Keys', command = '', width = 20).grid(row = 3, column = 1)

        shutdown_button = Button(features, text = 'Refresh client list', command = '', width = 20).grid(row = 1, column = 3)
        drop_shell = Button(features, text = 'Drop to Shell', command = '', width = 20).grid(row = 2, column = 3)

        update_all = Button(features, text = 'Update All Clients', command = '', width = 20).grid(row = 1, column = 4)
        update = Button(features, text = 'Update Selected Client', command = '', width = 20).grid(row = 2, column = 4)

        shutdown_all_button = Button(features, text = 'Shutdown All Client', command = '', width = 20).grid(row = 1, column = 5)
        shutdown_button = Button(features, text = 'Shutdown Selected Client', command = '', width = 20).grid(row = 2, column = 5)

        reboot_all = Button(features, text = 'Reboot All Client', command = '', width = 20).grid(row = 1, column = 5)
        reboot = Button(features, text = 'Reboot Selected Client', command = '', width = 20).grid(row = 2, column = 5)

        server = LabelFrame(self, text = 'Server')
        server.grid(row = 0, column = 3)

        start_server_button = Button(server, text = 'Start Server', width = 20).grid(row = 0, column = 1)
        stop_server_button = Button(server, text = 'Stop Server', width = 20).grid(row = 1, column = 1)
        restart_server_button = Button(server, text = 'Restart Server', width = 20).grid(row = 2, column = 1)

        client_frame = LabelFrame(self, text = 'Clients Area', height = 400, width = 1400)
        client_frame.grid(row = 1, column = 1, columnspan = 3)

        Label(client_frame, text = 'Client list').grid(row = 0, column = 1)
        self.options['clients'] = Listbox(client_frame, width = 120, height = 30).grid(row = 1, column = 1)

        Label(client_frame, text = 'Log').grid(row = 0, column = 2)
        self.options['log'] = Text(client_frame, foreground = 'white', background = 'black', height = 32)
        self.options['log'].grid(row = 1, column = 2)

    def create_key(self):
        key = gen_string()
        self.options['key'].set(key)
    def date_time(self):
        while True:
            self.title(string = '<< Remote Administration Tool | Control Panel  | %s %s >>' % (time.strftime('%x'), time.strftime('%X')))
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
