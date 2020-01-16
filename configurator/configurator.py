#!/usr/bin/env python

import paramiko

class Configurator(object):
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.WarningPolicy())

    def run_command(self, cmd, servers, username, password):
        for server in servers:
            try:
                print("*** Connecting to {}...***".format(server))
                self.client.connect(server, username=username, password=password)
                print("*** Successfullt connected ***")
                stdin, stdout, stderr = self.client.exec_command(cmd)
                for line in stdout:
                    print('... ' + line.strip('\n'))
                self.client.close()
            except Exception as e:
                print(e)


def main():
    c = Configurator()
    c.run_command('ls', ['18.191.242.16', '13.59.83.101'], 'ntata', 'tiptop123')

if __name__ == '__main__':
    main()
