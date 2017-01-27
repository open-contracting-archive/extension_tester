#!/usr/bin/env python
from __future__ import print_function
import unittest
import os 
import json
import requests
import json_merge_patch
import copy
from jsonschema.validators import Draft4Validator as validator
from jsonschema import FormatChecker

current_dir = os.path.dirname(os.path.realpath(__file__))
all_json_path = {}
all_json_data = {}
all_schema_data = {}

with open(os.path.join(current_dir, 'fixtures' ,"fullfakedata.json")) as fakedata_file:
    fakedata = json.load(fakedata_file)

def gather_data():

    schema_dir = os.getcwd()

    schema_list_page = requests.get('http://standard.open-contracting.org/schema').text

    parts = schema_list_page.split('href="')
    all_versions = []
    for part in parts:
        start = part[:part.find('"')].strip("/")
        version_parts = tuple(start.split("__"))
        if len(version_parts) != 3 or version_parts[-1] == "RC":
            continue
        all_versions.append(version_parts)
    all_versions.sort()
    latest_version = "__".join(all_versions[-1])


    all_json = ["release-package-schema.json", "release-schema.json", 
                "record-package-schema.json", "versioned-release-validation-schema.json", 
                "extension.json"]

    for file_name in all_json:
        if file_name == "extension.json":
            continue
        all_schema_data[file_name] = requests.get('http://standard.open-contracting.org/schema/' + latest_version + '/' + file_name).json()



    for file_name in all_json:
        file_path = os.path.join(schema_dir, file_name)
        try:
            with open(file_path) as json_file:
                all_json_path[file_name] = file_path
                try:
                    all_json_data[file_name] = json.load(json_file)
                except json.decoder.JSONDecodeError:
                    # ignore for now as tests will catch this
                    all_json_data[file_name] = {}
        except IOError:
            if file_name == "extension.json":
                raise Exception("extension.json not found. This directroy is not an extension or the extension.json file is missing")
            print("Warning File {} not found in this extension".format(file_name))


gather_data()


class TestExtensions(unittest.TestCase):

    def test_valid_json(self):
        for file_name, json_file_name in all_json_path.items():
            with open(json_file_name) as json_file:
                try:
                    json.load(json_file)
                except json.decoder.JSONDecodeError:
                    raise Exception("File {} can does not appear to be valid JSON".format(file_name))

    def test_patches_apply(self):
        for key, schema in all_schema_data.items():
            new_schema = copy.deepcopy(schema)
            if key in all_json_data:
                new_schema = json_merge_patch.merge(new_schema, all_json_data[key])
                if new_schema != schema:
                    print("{} has been patched".format(key))

    def test_fakedata(self):
        self.assertTrue(validator(all_schema_data["release-package-schema.json"], format_checker=FormatChecker()).is_valid(fakedata))
        

def run_tests():
    unittest.main()


if __name__ == '__main__':
    run_tests()
