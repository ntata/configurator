import paramiko
import sys
import os

class SshConnection():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        if 'CONFIGURATOR_SSH_USER' not in os.environ or 'CONFIGURATOR_SSH_USER_PASSWORD' not in os.environ:
            print("Please set CONFIGURATOR_SSH_USER and CONFIGURATOR_SSH_USER_PASSWORD environment variable")
            sys.exit(1)
        else:
            self.user = os.environ.get('CONFIGURATOR_SSH_USER', 'dummy')
            self.password = os.environ.get('CONFIGURATOR_SSH_USER_PASSWORD', 'dummy')

    def run_command(self, cmd, server):
        output = []
        error = []
        #print("*** Connecting to {}...***\n\n".format(server))
        self.client.connect(server, username=self.user, password=self.password)
        #print("*** Successfully connected ***\n\n")
        #print("*** Running '{}' on '{}'***\n\n".format(cmd, server))
        if 'sudo' in cmd:
            cmd = "echo '{}' | ".format(self.password) + cmd.replace('sudo', 'sudo -S')
        stdin, stdout, stderr = self.client.exec_command(cmd)
        for line in stderr:
            error.append(line)
        for line in stdout:
            output.append(line)
        self.client.close()
        print("output is '{}' and error is '{}'".format(output, error))
        return output, error
