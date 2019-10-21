# -*- coding: utf-8 -*-

"""
JSS Categories
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.1.0"


def categories(api, name='', exclude=()):
    """
    Get JSS Categories

    :param api:              jamf.API object
    :param name  <str>:      name in category['name']    
    :param exclude  <iter>:  category['name'] not in exclude
    
    :returns:  list of dicts: [{'id': jssid, 'name': name}, ...]
    """
    # list of category dicts: [{'id': id, 'name': name}, ...]
    _categories = api.get('categories')['categories']['category']
    # exclude specified categories by full name
    included = [c for c in _categories if c['name'] not in exclude]
    #NOTE: empty string ('') always in all other strings
    return [c for c in included if name in c['name']]
