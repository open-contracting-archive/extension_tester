from setuptools import setup
setup(name='ocds-extension-tester',
      version='0.4',
      description='OCDS tool to test extensions',
      author='David Raznick',
      author_email='mr.raznick@gmail.com',
      install_requires=[
             'requests',
             'json-merge-patch',
             'jsonschema',
             'rfc3987',
             'strict-rfc3339'
      ],
      scripts=['ocds_extension_tester.py'],
      package_data={'ocds_extension_tests': ['fixtures/fullfakedata.json']},
      packages=['ocds_extension_tests'],
      license='BSD',
      url='https://github.com/open-contracting/extension-tester'
)
