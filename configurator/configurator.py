#!/usr/bin/env python

"""
######## configurator #########

Usage:
    configurator.py ([-h <hosts>...] -u <user> -p <password> ([-c <command>...] | [--install-pkg <packages>...] | [--uninstall-pkg <packages>...]) | -t <template>)

Options:
    -h hosts, --hosts hosts          # remote host to configure
    -u user, --user user             # ssh user
    -p password, --password password # ssh password for the user
    -c command, --run-cmd command    # command to run on remote host
    --install-pkg <packages>         # packages to install
    --uninstall-pkg <packages>          # packages to uninstall
    -t template, --template template # YAML template to run
    --help                           # Show this screen.
    --version                        # Show Version.
    --dry-run                        # Print the command string, don't actually run commands.
"""


from ssh import SshConnection
from packages import Packages
from template import Template
from files import File
from service import Service
from docopt import docopt
import sys
import os

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Configurator 0.1')
    commands = ''
    install_pkgs = ''
    uninstall_pkgs = ''
    upgrade_pkgs = ''
    pkg_service_deps = ''
    file_metadata = ''
    file_data = ''
    services = ''
    service_action = ''
    service_pkg_deps = ''
    if not arguments['--template']:
        hosts = arguments['--hosts']
        user = arguments['--user']
        password = arguments['--password']
        if arguments['--run-cmd']:
            commands = arguments['--run-cmd']
        elif arguments['--install-pkg']:
            install_pkgs = arguments['--install-pkg']
        elif arguments['--uninstall-pkg']:
            uninstall_pkgs = arguments['--uninstall-pkg']
    else:
        t = Template()
        template = arguments['--template']
        parsed = t.loadYamlFile(template, "templates")
        hosts = parsed['hosts']
        user = parsed['user']
        password = parsed['password']
        if 'run-cmd' in parsed['action'].keys():
            commands = parsed['action']['run-cmd']
        elif 'install-pkg' in parsed['action'].keys():
            install_pkgs = parsed['action']['install-pkg']
            pkg_service_deps = parsed['action']['service_deps']
        elif 'uninstall-pkg' in parsed['action'].keys():
            uninstall_pkgs = parsed['action']['uninstall-pkg']
        elif 'upgrade-pkg' in parsed['action'].keys():
            upgrade_pkgs = parsed['action']['upgrade-pkg']
        elif 'create-file' in parsed['action'].keys():
            file_metadata = parsed['action']['create-file']['metadata']
            file_data = parsed['action']['create-file']['data']
        elif 'delete-file' in parsed['action'].keys():
            file_metadata = parsed['action']['delete-file']['metadata']
        elif 'service_name' in parsed['action'].keys():
            service_action = parsed['action']['service_action']
            services = parsed['action']['service_name']
            service_pkg_deps = parsed['action']['pkg_deps']
    try:
        c = SshConnection()
        s = Service()
        for host in hosts:
            if commands:
                for command in commands:
                    output, error = c.run_command(command, host, user, password)
                    if error != []:
                        raise Exception(error[0])
                    else:
                        print("\n*** Output of '{}' on '{}'".format(command, host))
                    for o in output:
                        print(o.strip('\n'))
            elif install_pkgs:
                p = Packages()
                p.install_package(host, install_pkgs, user, password)
                s = Service()
                s.manageService(pkg_service_deps, 'restart', service_pkg_deps, host, user, password)
            elif uninstall_pkgs:
                p = Packages()
                p.uninstall_package(host, uninstall_pkgs, user, password)
            elif upgrade_pkgs:
                p = Packages()
                p.upgrade_package(host, upgrade_pkgs, user, password)
            elif file_data and file_metadata:
                f = File()
                f.create_file(host, file_data, file_metadata, user, password)
            elif not file_data and file_metadata:
                f = File()
                f.delete_file(host, file_metadata, user, password)
            elif services:
                s.manageService(services, service_action, service_pkg_deps, host, user, password)
    except Exception as e:
        print(e)
