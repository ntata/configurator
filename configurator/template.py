import os
import yaml
import sys


class Template:
    def __init__(self):
        pass

    def templateSelector(self, name):
        templates_path = os.path.join(os.getcwd(), "templates")
        try:
            if os.path.isfile(os.path.join(templates_path, name)):
                return os.path.join(templates_path, name)
        except Exception as e:
            print(e)
            sys.exit(1)

    def loadTemplate(self, name):
        template_file = self.templateSelector(name)
        try:
            result = {}
            with open(template_file, 'r') as f:
                parsed = yaml.load(f.read(), yaml.SafeLoader)
            return parsed
        except Exception as e:
            print(e)
            sys.exit(1)
