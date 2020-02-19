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
from docopt import docopt

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Configurator 0.1')
    c = SshConnection()
    t = Template()
    commands = ''
    install_pkgs = ''
    uninstall_pkgs = ''
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
        template = arguments['--template']
        parsed = t.loadTemplate(template)
        hosts = parsed['hosts']
        user = parsed['user']
        password = parsed['password']
        if 'run-cmd' in parsed['action'].keys():
            commands = parsed['action']['run-cmd']
        elif 'install-pkg' in parsed['action'].keys():
            install_pkgs = parsed['action']['install-pkg']
        elif 'uninstall-pkg' in parsed['action'].keys():
            uninstall_pkgs = parsed['action']['uninstall-pkg']
    try:
        for host in hosts:
            if commands:
                for command in commands:
                    output, error = c.run_command(command, host, user, password)
                    print("\n*** Output of '{}' on '{}'".format(command, host))
                    for o in output:
                        print(o.strip('\n'))
            elif install_pkgs:
                p = Packages()
                p.install_package(host, install_pkgs, user, password)
            elif uninstall_pkgs:
                p = Packages()
                p.uninstall_package(host, uninstall_pkgs, user, password)
    except Exception as e:
        print(e)
