#!/usr/bin/env python

"""
######## configurator #########

Usage:
    configurator.py runcmd ([-h <hosts>...] -u <user> -p <password> -c <command> | -t <template>)

Options:
    -h hosts, --hosts hosts          # remote host to configure
    -u user, --user user             # ssh user
    -p password, --password password # ssh password for the user
    -c command, --command command    # command to run on remote host
    -t template, --template template # YAML template to run
    --help                           # Show this screen.
    --version                        # Show Version.
    --dry-run                        # Print the command string, don't actually run commands.
"""


from ssh import SshConnection
from packages import Packages
from template import Template
from docopt import docopt

#def main():
#    p = Packages()
#    p.install_package(['18.191.242.16', '13.59.83.101'], ['vim'])
#    p.delete_package(['18.191.242.16', '13.59.83.101'], ['vim'])

if __name__ == '__main__':
    arguments = docopt(__doc__, version='Configurator 0.1')
    #print(arguments)
    c = SshConnection()
    t = Template()
    if arguments['runcmd']:
        if arguments['--template'] is None:
            servers = arguments['--hosts']
            user = arguments['--user']
            password = arguments['--password']
            command = arguments['--command']
        else:
            template = arguments['--template']
            parsed = t.loadTemplate(template)
            servers = parsed['hosts']
            user = parsed['user']
            password = parsed['password']
            command = parsed['action']['runcmd']['command']
    try:
        for server in servers:
            output = c.run_command(command, server, user, password)
            print("\n*** Output of '{}' on '{}'".format(command, server))
            for o in output:
                print(o.strip('\n'))
    except Exception as e:
        print(e)
