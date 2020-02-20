import os
import yaml
import sys


class Template:
    def __init__(self):
        pass

    def yamlFileSelector(self, filename, filefolder):
        yaml_file_path = os.path.join(os.getcwd(), filefolder)
        try:
            if os.path.isfile(os.path.join(yaml_file_path, filename)):
                return os.path.join(yaml_file_path, filename)
        except Exception as e:
            print(e)
            sys.exit(1)

    def loadYamlFile(self, filename, filefolder):
        yaml_file= self.yamlFileSelector(filename, filefolder)
        try:
            result = {}
            with open(yaml_file, 'r') as f:
                parsed = yaml.load(f.read(), yaml.SafeLoader)
            return parsed
        except Exception as e:
            print(e)
            sys.exit(1)
