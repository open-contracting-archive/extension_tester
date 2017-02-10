Open Contracting Data Standard Extension Tester
===============================================

This library provides a simple way to do some basic tests on your OCDS extension.

Installation
-------------

This can be done locally inside a virtual enviroment or globally.

```
pip install ocds-extension-tester
```
or clone the repository and paste:
```
python setup.py install
```
or for development use:
```
python setup.py develop
```
This requires setuptools to be installed.

Usage
------

Change directory to the directory where you OCDS extension lives. ie:

```
cd ~/myocdsextension
```

run

```
ocds_extension_tester.py
```

This will run the tests on that extension.


If you just want to test a full schema directory and not just an extension, not just an extension:

TEST_CORE=1 ocds_extension_tester.py
