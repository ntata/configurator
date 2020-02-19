from ssh import SshConnection
import sys

class Packages():
    def __init__(self):
        pass

    def check_if_valid_package(self, package, host, user, password):
        cmd = "apt-cache search --names-only '^{}'".format(package)
        c = SshConnection()
        output, error = c.run_command(cmd, host, user, password)
        if error == [] and output == []:
            print("\n\n*** Not a valid package. Please check the package name or the apt repositories")
            sys.exit(1)
        else:
            return True


    def check_if_package_installed(self, package, host, user, password):
        cmd = "dpkg -L {} | grep 'is not installed'".format(package)
        try:
            c = SshConnection()
            output, error = c.run_command(cmd, host, user, password)
            if error == []:
               print("*** '{}' is already installed on '{}'\n\n".format(package, host))
               return True
            else:
                print("*** '{}' is currently not installed on '{}'\n\n".format(package, host))
                return False
        except Exception as e:
            print(e)
            sys.exit(1)
    
    def install_package(self, host, packages, user, password):
        for package in packages:
           print("*** Checking to see if '{}' is already installed on '{}'\n\n".format(package, host))
           if self.check_if_valid_package(package, host, user, password):
               pass
           if self.check_if_package_installed(package, host, user, password):
               continue
           else:
               try:
                   print("\n*** Proceeding to install '{}'\n".format(package))
                   cmd = "sudo apt-get update && sudo apt-get install {} -y".format(package)
                   c = SshConnection()
                   output, error = c.run_command(cmd, host, user, password)
                   if error[-1] == "E: Unable to locate package php\n":
                       raise Exception("E: Unable to locate package php\n")
                   for o in output:
                       print(o.strip('\n'))
                   print("*** Successfully installed '{}' on '{}'\n\n".format(package, host))
               except Exception as e:
                   print(e)
                   sys.exit(1)
    
    def uninstall_package(self, host, packages, user, password):
        for package in packages:
            print("*** Checking for '{}' package on '{}'\n\n".format(package, host))
            if not self.check_if_package_installed(package, host, user, password):
                print("Nothing to uninstall; '{}' is not installed on '{}'\n\n".format(package, host))
                continue
            else:
                try:
                    print("\nUninstalling '{}' on '{}'\n".format(package, host))
                    cmd = "sudo apt-get remove {} -y && sudo apt-get autoremove -y".format(package)
                    c = SshConnection()
                    output, error = c.run_command(cmd, host, user, password)
                    for o in output:
                        print(o.strip('\n'))
                    print("*** Successfully uninstalled '{}' from '{}'\n\n".format(package, host))
                except Exception as e:
                    print(e)
                    sys.exit(1)
