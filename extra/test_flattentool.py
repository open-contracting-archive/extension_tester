import json_merge_patch
import flattentool
import traceback
import requests
import json
import copy
import os

release_schema = requests.get('http://standard.open-contracting.org/schema/1__1__0/release-schema.json').json()

os.makedirs('extended_schemas', exist_ok=True)

with open('ocds-213czf-000-00001-01-planning.json', 'w') as fp:
    fp.write(requests.get('https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/1.1/ocds-213czf-000-00001-01-planning.json').text)


def try_flattentool(schema_path):
    flattentool.flatten(
        # https://raw.githubusercontent.com/open-contracting/sample-data/master/fictional-example/ocds-213czf-000-00001-01-planning.json
        'ocds-213czf-000-00001-01-planning.json',
        root_id='ocid',
        main_sheet_name='releases',
        output_name='flattened',
        root_list_path='releases',
        schema=schema_path
    )

    flattentool.unflatten(
        'flattened.xlsx',
        root_id='ocid',
        input_format='xlsx',
        output_name='release.json',
        root_list_path='releases',
        schema=schema_path
    )

# Run once with the base 1.1 schema, so its clear which warnings are from that
try_flattentool('http://standard.open-contracting.org/schema/1__1__0/release-schema.json')

extensions_list = requests.get('http://standard.open-contracting.org/extension_registry/master/extensions.json').json()['extensions']
extensions_dict = {e['slug']:e for e in extensions_list}

for extension in extensions_list:
    extended_schema = copy.deepcopy(release_schema)

    def do_patch(extension):
        release_schema_patch = requests.get(extension['url']+'release-schema.json').json()
        json_merge_patch.merge(extended_schema, release_schema_patch)

    if extension['slug'] == 'bids':
        do_patch(extensions_dict['requirements'])
    elif extension['slug'] == 'transaction_milestones':
        do_patch(extensions_dict['metrics'])
    do_patch(extension)

    schema_path = os.path.join('extended_schemas', extension['slug']+'.json')
    with open(schema_path, 'w') as fp:
        json.dump(extended_schema, fp, indent=4)

    print(extension['slug'])

    try:
        try_flattentool(schema_path=schema_path)
    except:
        traceback.print_exc()
