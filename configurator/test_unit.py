from template import Template
import unittest
from unittest.mock import patch
import os
import paramiko
from ssh import SshConnection
from packages import Packages
import mock

class ConfiguratorTestCases(unittest.TestCase):
    def setUp(self):
        pass

    def test_yamlFileSelector(self):
        t = Template()
        yaml_file = t.yamlFileSelector('create_file.yaml', "templates")
        assert os.path.isfile(yaml_file) == True

    def test_loadYamlFile(self):
        t = Template()
        parsed = t.loadYamlFile('run_cmd.yaml', 'templates')
        assert list(parsed['action'].keys())[0] == 'run-cmd'

    @mock.patch('packages.Packages.check_if_valid_package', return_value=True)
    def test_check_if_valid_package(self, mock_check_if_valid_package):
        p = Packages()
        assert mock_check_if_valid_package is p.check_if_valid_package
        assert mock_check_if_valid_package('vim') == True

    @mock.patch('packages.Packages.check_if_package_installed', return_value=True)
    def test_check_if_package_installed(self, mock_check_if_package_installed):
        p = Packages()
        assert mock_check_if_package_installed is p.check_if_package_installed
        assert mock_check_if_package_installed('vim') == True

if __name__ == '__main__':
    unittest.main()
