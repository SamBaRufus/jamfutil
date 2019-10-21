# -*- coding: utf-8 -*-

"""
Tests for jamf.policy
"""

import unittest
import logging
from .. import policy

# suppress logging messages
logging.getLogger(__name__).addHandler(logging.NullHandler())


class MockAPI(object):
    
    def __init__(self, data):
        self.data = data
    
    def get(self, endpoint):
        return self.data[endpoint]

    def put(self, endpoint, data):
        return data


class PackageTestCase(unittest.TestCase):
    
    def setUp(self):
        _policy = {'general': {'id': '1'}, 
                  'package_configuration': {'packages': {'size': '0'}}}
        self.data = {'policy': _policy}
        _data = {'policies/name/test': self.data,
                 'policies/id/1': self.data}
        self.api = MockAPI(_data)
        self.policy = policy.Policy(self.api, name='test')


class TestPolicyPackages(PackageTestCase):
    
    def test_packages_is_not_none(self):
        self.assertIsNotNone(self.policy.packages)

    def test_packages_access(self):
        orig = self.policy.data['package_configuration']['packages']
        self.assertIsNot(orig, self.policy.packages)        

    def test_packages_identity_mod(self):
        expected = [{'id': 1}]
        self.policy.packages = [{'id': 1}]
        ref = self.policy.data['package_configuration']['packages']['package']
        self.assertEqual(self.policy.packages, expected)
        self.assertIs(self.policy.packages, ref)

    def test_packages_modify_dict(self):
        expected = [{'id': 1}]
        self.policy.packages = {'id': 1}
        self.assertEqual(self.policy.packages, expected)
        
    def test_packages_modify_list(self):
        expected = [{'id': 1}]
        self.policy.packages = [{'id': 1}]
        self.assertEqual(self.policy.packages, expected)
        
    def test_packages_modify_tuple(self):
        expected = [{'id': 1},]
        self.policy.packages = ({'id': 1},)
        self.assertEqual(self.policy.packages, expected)


class TestPolicyAddPackage(PackageTestCase):

    def test_add_package(self):
        """
        test adding a package produces correct result
        """
        expected = [{'name': 'test.pkg', 'action': 'Install'}]
        self.policy.add_package('test.pkg')
        result = self.policy.packages
        self.assertEqual(expected, result)

    def test_add_package_action(self):
        """
        test adding package '' raises policy.Error
        """
        self.policy.add_package('test.pkg', action="Uninstall")
        expected = [{'name': 'test.pkg', 'action': 'Uninstall'}]
        result = self.policy.packages
        self.assertEqual(expected, result)
        
    def test_add_duplicate_package_action(self):
        """
        test adding same package and action raises policy.Error
        """
        self.policy.add_package("test.pkg", action='Cache')
        with self.assertRaises(policy.Error):
            self.policy.add_package("test.pkg", action='Cache')
        
    def test_add_None_package(self):
        """
        test adding package None raises policy.Error
        """
        with self.assertRaises(policy.Error):
            self.policy.add_package(None)
        
    def test_add_package_empty(self):
        """
        test adding package '' raises policy.Error
        """
        with self.assertRaises(policy.Error):
            self.policy.add_package('')
        
    def test_add_same_package_different_actions(self):
        """
        test adding the same package with another action succeeds
        """
        self.policy.add_package('test.pkg', action='Cache')
        self.policy.add_package('test.pkg', action='Install Cached')
        expected = [{'name': 'test.pkg', 'action': 'Cache'},
                    {'name': 'test.pkg', 'action': 'Install Cached'}]
        result = self.policy.packages
        self.assertEqual(expected, result)
        

class TestPolicyRemovePackage(PackageTestCase):
    
    def setUp(self):
        super().setUp()
        self.policy.add_package('test.pkg')
        
    def test_remove_package(self):
        """
        test adding a package produces correct result
        """
        self.policy.remove_package('test.pkg')
        self.assertEqual(self.policy.packages, [])

    def test_remove_missing_package(self):
        """
        test adding same package raises policy.Error
        """
        self.policy.packages = []
        with self.assertRaises(policy.Error):
            self.policy.remove_package('test.pkg')
        
    def test_remove_None_package(self):
        """
        test removing package None raises policy.Error
        """
        with self.assertRaises(policy.Error):
            self.policy.remove_package(None)
        
    def test_add_package_empty(self):
        """
        test remove package '' raises policy.Error
        """
        with self.assertRaises(policy.Error):
            self.policy.remove_package('')

    def test_remove_all(self):
        """
        test all packages are removed
        """
        self.policy.add_package("test2.pkg")
        self.policy.remove_all_packages()
        self.assertEqual(self.policy.packages, [])
   

if __name__ == '__main__':
    unittest.main(verbosity=2)
