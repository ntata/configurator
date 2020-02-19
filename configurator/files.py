import sys
import os
from ssh import SshConnection

class File():
    def __init__(self):
        pass

    def check_if_file_exists(self, host, file_metadata, file_path, user, password):
        cmd = "test -e {} && echo file exists || echo file not found".format(file_path)
        try:
            c = SshConnection()
            output, error = c.run_command(cmd, host, user, password)
            if output[0] == 'file exists\n':
                return True
            else:
                return False
        except Exception as e:
            print(e)


    def set_file_permissions(self, host, file_metadata, file_path, user, password):
        cmd1 = "sudo chown {}:{} {}".format(file_metadata['user_owner'], file_metadata['group_owner'], file_path)
        cmd2 = "sudo chmod {} {}".format(file_metadata['numeric_mode'], file_path)
        try:
            c = SshConnection()
            output, error = c.run_command(cmd1+'&&'+cmd2, host, user, password)
            if error == []:
                print("\n\n*** Set permissions on {} on {}".format(file_path, host))
        except Exception as e:
            print(e)


    def create_file(self, host, file_data, file_metadata, user, password):
        file_path = file_metadata['path']+'/'+file_metadata['name']
        cmd = "echo '{}' | sudo tee {}".format(file_data, file_path)
        try:
            if self.check_if_file_exists(host, file_metadata, file_path, user, password):
                raise Exception("File already exists on {}!".format(host))
            c = SshConnection()
            output, error = c.run_command(cmd, host, user, password)
            if error != []:
                raise Exception(error[0]+"on {}".format(host))
            #for o in output:
            #    print(o.strip('\n'))
            print("\n\n*** Created file {} on {}".format(file_path, host))
            self.set_file_permissions(host, file_metadata, file_path, user, password)
        except Exception as e:
            print(e)

    def delete_file(self, host, file_metadata, user, password):
        file_path = file_metadata['path']+'/'+file_metadata['name']
        cmd = "sudo rm {}".format(file_path)
        try:
            if not self.check_if_file_exists(host, file_metadata, file_path, user, password):
                raise Exception("File doesn't exist on {}!".format(host))
            c = SshConnection()
            output, error = c.run_command(cmd, host, user, password)
            if error != []:
                raise Exception(error[0]+"on {}".format(host))
            for o in output:
                print(o.strip('\n'))
            print("\n\n*** Deleted {} on {}".format(file_path, host))
        except Exception as e:
            print(e)
