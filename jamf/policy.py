# -*- coding: utf-8 -*-

"""
JAMF Policy functions
"""

__author__ = 'Sam Forester'
__email__ = 'sam.forester@utah.edu'
__copyright__ = 'Copyright (c) 2019 University of Utah, Marriott Library'
__license__ = 'MIT'
__version__ = "0.0.0"

import logging


class Error(Exception):
    pass


class Policy(object):

    def __init__(self, api, name=None, jssid=None):
        self.log = logging.getLogger(f"{__name__}.Policy")
        self.api = api
        self._packages = None

        if jssid:
            _endpoint = f"policies/id/{jssid}"
        elif name:
            _endpoint = f"policies/name/{name}"
            self.data = api.get(f"policies/name/{name}")['policy']
            self.jssid = self.data['general']['id']
        else:
            raise Error("must specify name or policy ID")
        
        self.data = api.get(_endpoint)['policy']
        self.jssid = self.data['general']['id']        
        self.endpoint = f"policies/id/{self.jssid}"

    @property
    def packages(self):
        if not self._packages:
            self._packages = {'package': []}
            pkgs = self.data['package_configuration']['packages']   
            size = int(pkgs.get('size', len(pkgs.get('package', []))))
            if size == 1:
                self._packages['package'].append(pkgs['package'])
            elif size > 1:
                self._packages['package'] = pkgs['package']
            self.data['package_configuration']['packages'] = self._packages
        return self._packages['package']

    @packages.setter
    def packages(self, x):
        if not self._packages:
            self._packages = {'package': []}
            self.data['package_configuration']['packages'] = self._packages
        if isinstance(x, dict):
            self._packages['package'].append(x)
        elif isinstance(x, list):
            self._packages['package'] = x
        else:
            self._packages['package'] = [y for y in x]
        
    def add_package(self, name, action='Install'):
        """
        Add package to policy (by name)

        :param name  <str>:    name of JSS package
        :param action  <str>:  package action (default: 'Install')
        """
        if not name:
            raise Error(f"invalid package name: {name}")

        pkg = {'name': name, 'action': action}
        existing = [x for x in self.packages if x != pkg]
        
        if len(existing) != len(self.packages):
            raise Error("policy already contains package: %r", name)

        self.packages.append({'name': name, 'action': action})
        result = self.api.put(self.endpoint, {'policy': self.data})
        self.log.info(f"added package: {name}")
        return result
        
    def remove_package(self, name):
        """
        Remove package from policy (by name)

        :param name  <str>:    name of JSS package
        """
        if not name:
            raise Error(f"invalid package name: {name}")

        modified = [x for x in self.packages if x['name'] != name]

        if len(modified) == len(self.packages):
            raise Error("policy missing package: %r", name)

        self.packages = modified
        self.api.put(self.endpoint, {'policy': self.data})
        self.log.info(f"removed package: {name}")

    def remove_all_packages(self, name=None):
        """
        remove all package from policy
        """
        self.packages = []
        return self.api.put(self.endpoint, {'policy': self.data})


def policies_in_categories(api, names):
    """
    Get list of policies in specified categories

    :param api:         jamf.API object
    :param categories:  list of category names
    :returns:           list of all policies from specified categories
    """
    logger = logging.getLogger(__name__)
    logger.debug(f"categories: {categories}")
    policies = []
    for category in names:
        result = api.get(f"policies/category/{category}")['policies']
        policies += result.get('policy', [])
    
    return policies

