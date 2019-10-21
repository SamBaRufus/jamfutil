# -*- coding: utf-8 -*-

"""
Tests for jamf.convert
"""

import unittest
from .. import convert


class ConversionTest(unittest.TestCase):
    
    def setUp(self):
        self.xml = '<nothing/>'
        self.data = {'nothing': None}
    
    def test_xml_to_dict(self):
        """
        test conversion of xml string to dict 
        """
        expected = self.data
        result = convert.xml_to_dict(self.xml)
        self.assertEqual(expected, result)

    def test_dict_to_xml(self):
        """
        test conversion of dict to xml string
        """
        expected = self.xml
        result = convert.dict_to_xml(self.data)
        self.assertEqual(expected, result)

    def test_dict_reconvert(self):
        """
        test dict -> xml -> dict
        """
        _xml = convert.dict_to_xml(self.data)
        result = convert.xml_to_dict(_xml)
        expected = self.data
        self.assertEqual(expected, result)

    def test_xml_reconvert(self):
        """
        test xml -> dict -> xml
        """
        _dict = convert.xml_to_dict(self.xml)
        result = convert.dict_to_xml(_dict)
        expected = self.xml
        self.assertEqual(expected, result)


class TestSimpleDict(ConversionTest):

    def setUp(self):
        self.xml = '<test><key>value</key></test>'
        self.data = {'test': {'key': 'value'}}


class TestSimpleList(ConversionTest):
    
    def setUp(self):
        self.xml = ('<list>'
                      '<item>one</item>'
                      '<item>two</item>'
                      '<item>three</item>'
                    '</list>')
        self.data = {'list': {'item': ['one', 'two', 'three']}}
        

class TestListOfDicts(ConversionTest):
    
    def setUp(self):
        self.xml = ('<list>'
                      '<item>'
                        '<id>1</id>'
                        '<name>one</name>'
                      '</item>'
                      '<item>'
                        '<id>2</id>'
                        '<name>two</name>'
                      '</item>'
                      '<item>'
                        '<id>3</id>'
                        '<name>three</name>'
                      '</item>'
                    '</list>')
        self.data = {'list': {'item': [{'id': '1', 'name': 'one'}, 
                                       {'id': '2', 'name': 'two'},
                                       {'id': '3', 'name': 'three'}]}}


if __name__ == '__main__':
    unittest.main(verbosity=2)
