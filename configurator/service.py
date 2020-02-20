import sys
import os
from ssh import SshConnection
from template import Template
from packages import Packages

class Service():
    def __init__(self):
        pass

    def getServiceDependencies(self, service):
        t = Template()
        try:
            service_dep_mapping = t.loadYamlFile('service_dependencies.yaml', os.getcwd())
            for item in service_dep_mapping['service']:
                if list(item.keys())[0] == service:
                    file_deps = item[service]['file_deps']
                    pkg_deps = item[service]['package_deps']
                    return file_deps, pkg_deps
        except Exception as e:
            print(e)
            raise e


    def manageService(self, service, service_action, host, user, password):
        try:
            # check if package dependencies are already installed. If not, install them now
            if service_action == 'start' or 'restart':
                file_dps, pkg_dps = self.getServiceDependencies(service)
                p = Packages()
                pkgs_to_install = []
                print("\n\n*** Checking dependencies...")
                for pkg in pkg_dps:
                    if p.check_if_package_installed(pkg, host, user, password):
                        pass
                    else:
                        pkgs_to_install.append(pkg)
                p.install_package(host, pkgs_to_install, user, password)
            if service_action == 'stop':
                pass
            print("\n\n*** {}ing {} service on {}".format(service_action, service, host))
                
            cmd = "sudo service {} {}".format(service, service_action)
            c = SshConnection()
            output, error = c.run_command(cmd, host, user, password)
            if error == []:
                for o in output:
                    print(o.strip('\n'))
            else:
                raise Exception(error[0])
        except Exception as e:
            print(e)

