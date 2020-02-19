import paramiko
import sys

class SshConnection():
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        #self.username = 'ntata'
        #self.password = 'tiptop123'

    def run_command(self, cmd, server, user, password):
        output = []
        error = []
        #print("*** Connecting to {}...***\n\n".format(server))
        self.client.connect(server, username=user, password=password)
        #print("*** Successfully connected ***\n\n")
        #print("*** Running '{}' on '{}'***\n\n".format(cmd, server))
        if 'sudo' in cmd:
            cmd = "echo '{}' | ".format(password) + cmd.replace('sudo', 'sudo -S')
        #print(cmd)
        stdin, stdout, stderr = self.client.exec_command(cmd)
        for line in stderr:
            error.append(line)
        for line in stdout:
            output.append(line)
        self.client.close()
        #if not output and not error:
        #    return stderr, output
        return output, error
