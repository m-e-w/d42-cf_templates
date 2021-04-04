import os
import yaml
import json
from device42 import Device42Api

with open('templates.yaml', 'r') as tmp:
    templates = yaml.load(tmp.read())

with open('config.yaml', 'r') as cfg:
    config = yaml.load(cfg.read())

options = config['options']
device42 = config['device42']
device42_api = Device42Api(device42, options)
dry_run = options['dry_run']
debug = options['debug']
use_bulk_fields = options['bulk_fields']
import_doql = options['import_doql']

def find_endpoint(x):
    return {
        'affinity_group': '/api/1.0/custom_fields/affinity_group/',
        'appcomp' : '/api/1.0/custom_fields/appcomp/',
        'asset' : '/api/1.0/custom_fields/asset/',
        'building': '/api/1.0/custom_fields/building/',
        'businessapp': '/api/1.0/custom_fields/businessapp/',
        'cable': '/api/1.0/custom_fields/cable/',
        'circuit': '/api/1.0/custom_fields/circuit/',
        'certificate': '/api/1.0/custom_fields/certificate/',
        'customer': '/api/1.0/customer/custom_field/',
        'databaseinstance': '/api/1.0/custom_fields/databaseinstance/',
        'device': '/api/1.0/device/custom_field/',
        'dns_records': '/api/dns_records/custom_field/',
        'dns_zone': '/api/1.0/custom_fields/dns_zone/',
        'endusers': '/api/1.0/custom_fields/endusers/',
        'hardware': '/api/1.0/custom_fields/hardware/',
        'ip_address': '/api/1.0/custom_fields/ip_address/',
        'part' : '/api/1.0/custom_fields/part/',
        'partmodel': '/api/1.0/custom_fields/partmodel/',
        'password': '/api/1.0/custom_fields/password/',
        'switchport': '/api/1.0/custom_fields/switchport/',
        'pdu': '/api/1.0/custom_fields/pdu/',
        'purchase': '/api/1.0/custom_fields/purchase/',
        'rack': '/api/1.0/custom_fields/rack/',
        'resource': '/api/1.0/custom_fields/resource/',
        'room': '/api/1.0/custom_fields/room/',
        'service': '/api/1.0/custom_fields/service/',
        'serviceinstance': '/api/1.0/custom_fields/serviceinstance/',
        'software': '/api/1.0/custom_fields/software/',
        'softwareinuse': '/api/1.0/custom_fields/softwareinuse/',
        'subnet': '/api/1.0/custom_fields/subnet/',
        'vendor': '/api/1.0/custom_fields/vendor/',
        'switch_vlan': '/api/1.0/custom_fields/switch_vlan/',
        'vrfgroup': '/api/1.0/custom_fields/vrfgroup/'    
    }.get(x, 'Undefined')

def get_value(value, row):
    if value.startswith('$'):
        value = value[1:]
        if row[value] is None:
            value = 'None'
        else:
            value = row[value]
    return value

def module_bulk_field(row, unique_id, ci_type, cf_endpoint, template):
    bulk_fields = []
    data = {}
   
    if row[unique_id]:
        if ci_type == 'device':
            data['device_id'] = row[unique_id]
        else:
            data['id'] = row[unique_id]

        for cf in template['custom_fields']:
            key = cf
            value = template['custom_fields'][cf]['value']
            value = get_value(value, row)
            kvp = key + ':' + value
            bulk_fields.append(kvp)

        data['bulk_fields'] = ",".join(bulk_fields)   
        if debug or dry_run:
            print('\tPayload: %s' % data)

        if(dry_run == False):
            response = device42_api._put_cf(data, cf_endpoint)
            print('\tPut:\t%s\tResponse: %s' % (cf_endpoint,response))
           
def module_normal(row, unique_id, ci_type, cf_endpoint, template):
    data = {}
    if row[unique_id]:
        if ci_type == 'device':
            data['device_id'] = row[unique_id]
        else:
            data['id'] = row[unique_id]
    for cf in template['custom_fields']:
        value = template['custom_fields'][cf]['value']
        data = dict(template['custom_fields'][cf])

        if ci_type == 'device':
            data['device_id'] = row[unique_id]
        else:
            data['id'] = row[unique_id]
        data['key'] = cf
        data['value'] = get_value(value, row)
        
        if debug or dry_run:
            print('\tPayload: %s' % data)

        if(dry_run == False):
            response = device42_api._put_cf(data, cf_endpoint)
            print('\tPut:\t%s\tResponse: %s' % (cf_endpoint,response))

def main(module):
    for template in templates: 
        print('\nLoading template: %s' % template)
        saved_doql_name = templates[template]['saved_doql']
        unique_id = templates[template]['unique_id']
        ci_type = templates[template]['ci_type']
        cf_endpoint = find_endpoint(ci_type)
       
        if(cf_endpoint != 'Undefined'):
            print('\nCalling saved DOQL query: %s' % saved_doql_name)
            results = device42_api._get_doql(saved_doql_name)
            if type(results) is not list:
                print(results)
            else:
                 for row in results: 
                     module(row, unique_id, ci_type, cf_endpoint, templates[template])
        else:
            print('API endpoint undefined, incorrect, or unsupported')

    
if __name__ == '__main__':
    if import_doql:
        path = 'template_doql/'
        doql_files = os.listdir(path)
        for file in doql_files:
            f = open(path + file)
            doql_query = f.read()
            response = device42_api._post_doql(file[:-4],doql_query)
            print(response)
    if use_bulk_fields:
        main(module_bulk_field)
    else:
        main(module_normal)