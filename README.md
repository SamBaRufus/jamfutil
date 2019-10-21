# jamfutil

Utility for updating Patch Management in JSS natively in Python

This is a util for maintaining Jamf Pro via command-line

# A Work in Progress

This library is nowhere near finished, I submitted it to allow a colleague to help with its development.

# Requirements

jamfutil requires python3 and requests library

# Authentication

Run the following command from inside the repo ('private/' is in .gitignore) 

```bash
$ mkdir private
$ cat <<EOT > private/jss.plist
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>login</key>
	<string>username:passwd</string>
	<key>address</key>
	<string>jamf.server.url</string>
</dict>
</plist>
EOT
```

The username and password provided will have to be added and given the appropriate access rights 

# Running Tests

```bash
$> cd jamfutil

# runs all tests
$> python3 -m unittest discover -v

# run tests individually
$> python3 -m jamf.tests.test_convert
```

# A Few Examples

The api can be interacted with via python3 shell

```bash
$> cd jamfutil
$> python3
```

```python
import pprint
import logging

import jamf

fmt = '%(asctime)s: %(levelname)8s: %(name)s - %(funcName)s(): %(message)s'
logging.basicConfig(level=logging.DEBUG, format=fmt)
logger = logging.getLogger(__name__)

# create an jamf.API object (requires requests lib)
logger.debug("creating api")
jss = jamf.API(config='private/jss.plist')

# get any information from your jss using the classic api endpoints

# print out all policies
all_policies = jss.get('policies')
pprint.pprint(all_policies)

# get all categories
categories = jamf.categories(jss)

category_names = [x['name'] for x in categories]

print(f"first category: {category_names[0]}")

# all policies in a for first and second category
policies = jamf.policy.policies_in_categories(jss, categories[0:2])
pprint.pprint(policies)
```

## Packages

As of `1.1` Policy packages can be modified using the following:

```python
import jamf

# create an jamf.API object (requires requests lib)
logger.debug("creating api")
jss = jamf.API(config='private/jss.plist')

policy = jamf.Policy(jss, name="Policy Name")

# add a package named "example.pkg" to the policy (must exist in JSS)
policy.add_package("example.pkg")

# remove "example.pkg" from the policy
policy.remove_package("example.pkg")

# add "example.pkg" to be cached
policy.add_package("example.pkg", action="Cache")

# remove all packages for policy
policy.remove_all_packages()

```


That's all I have currently
