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
        #import pdb; pdb.set_trace()
        try:
            result = {}
            with open(template_file, 'r') as f:
                parsed = yaml.load(f.read(), yaml.SafeLoader)
            #print(parsed)
            return parsed
        except Exception as e:
            print(e)
            sys.exit(1)
