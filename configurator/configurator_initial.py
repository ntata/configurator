#!/usr/bin/env python

import paramiko

class Configurator(object):
    def __init__(self):
        self.client = paramiko.SSHClient()
        self.client.load_system_host_keys()
        #self.client.set_missing_host_key_policy(paramiko.WarningPolicy())
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.username = 'ntata'
        self.password = 'tiptop123'

    def run_command(self, cmd, server):
            try:
                output = []
                #print("*** Connecting to {}...***\n\n".format(server))
                self.client.connect(server, username=self.username, password=self.password)
                #print("*** Successfully connected ***\n\n")
                print("*** Running '{}' on '{}'***\n\n".format(cmd, server))
                stdin, stdout, stderr = self.client.exec_command(cmd)
                for line in stdout:
                    output.append(line)
                self.client.close()
                return output
            except Exception as e:
                print(e)
                raise

    def check_if_package_installed(self, package, server):
        cmd = 'dpkg -s {} | grep Status'.format(package)
        try:
            output = self.run_command(cmd, server)
            if output != [] and output[0] == 'Status: install ok installed\n':
                print("*** {} is already installed on {}\n\n".format(package, server))
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def install_package(self, servers, packages):
        for server in servers:
            for package in packages:
                print("*** Checking to see if {} is already installed on {}\n\n".format(package, server))
                if self.check_if_package_installed(package, server):
                    continue
                else:
                    try:
                        print("*** Proceeding to install {}\n\n".format(package))
                        cmd = "echo 'tiptop123' | sudo -S apt-get update && sudo -S apt-get install {} -y".format(package)
                        output = self.run_command(cmd, server)
                        for o in output:
                            print(o.strip('\n'))
                        print("*** Successfully installed {} on {}\n\n".format(package, server))
                    except Exception as e:
                        print(e)
    
    def delete_package(self, servers, packages):
        for server in servers:
            for package in packages:
                print("*** Check to see if {} is installed and needs to be deleted\n\n".format(package))
                if not self.check_if_package_installed(package, server):
                    print("{} is not installed on the {}\n\n".format(package, server))
                    continue
                else:
                    try:
                        print("Uninstalling {} on {}\n\n".format(package, server))
                        cmd = "echo 'tiptop123' | sudo -S apt-get remove {} -y && sudo -S apt-get clean && sudo -S apt-get autoremove".format(package)
                        output = self.run_command(cmd, server)
                        for o in output:
                            print(o.strip('\n'))
                        print("*** Successfully uninstalled {} from {}\n\n".format(package, server))
                    except Exception as e:
                        print(e)


def main():
    c = Configurator()
    #try:
    #    for server in ['18.191.242.16', '13.59.83.101']:
    #        output = c.run_command("echo 'tiptop123' | sudo -S apt-get update", server)
    #        for o in output:
    #            print(o.strip('\n'))
    #except Exception as e:
    #    print(e)
    c.install_package(['18.191.242.16', '13.59.83.101'], ['vim'])
    #c.install_package(['18.191.242.16'], ['vim'])
    c.delete_package(['18.191.242.16', '13.59.83.101'], ['vim'])

if __name__ == '__main__':
    main()
