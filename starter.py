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

def find_endpoint(x):
    return {
        'building': '/api/1.0/custom_fields/building/',
        'room': '/api/1.0/custom_fields/room/',
        'rack': '/api/1.0/custom_fields/rack/',
        'device': '/api/1.0/device/custom_field/',
        'asset' : '/api/1.0/custom_fields/asset/',
        'part' : '/api/1.0/custom_fields/part/',
        'appcomp' : '/api/1.0/custom_fields/appcomp/'
    }.get(x, 'Undefined')

def module_bulk_field():
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
                    bulk_fields = []
                    data = {}
                    if row[unique_id]:
                        if ci_type == 'device':
                            data['device_id'] = row[unique_id]
                        else:
                            data['id'] = row[unique_id]

                        for cf in templates[template]['custom_fields']:
                            key = cf
                            value = templates[template]['custom_fields'][cf]['value']

                            if value.startswith('$'):
                                value = value[1:]
                                if row[value] is None:
                                    value = 'None'
                                else:
                                    value = row[value]
                            kvp = key + ':' + value
                            bulk_fields.append(kvp)

                        data['bulk_fields'] = ",".join(bulk_fields)   
                        if debug or dry_run:
                            print('\tPayload: %s' % data)

                        if(dry_run == False):
                            response = device42_api._put_cf(data, cf_endpoint)
                            print('\tPut:\t%s\tResponse: %s' % (cf_endpoint,response))

    
                
def module_normal():
    for template in templates: 
        print('\nLoading template: %s' % template)
        saved_doql_name = templates[template]['saved_doql']
        unique_id = templates[template]['unique_id']
        ci_type = templates[template]['ci_type']
        cf_endpoint = find_endpoint(ci_type)
       
        if(cf_endpoint != 'Undefined'):
            print('\nCalling saved DOQL query: %s' % saved_doql_name)
            results = device42_api._get_doql(saved_doql_name)
            
            for row in results: 
                for cf in templates[template]['custom_fields']:
                    cf_value = templates[template]['custom_fields'][cf]['value']
                    data = dict(templates[template]['custom_fields'][cf])

                    if ci_type == 'device':
                        data['device_id'] = row[unique_id]
                    else:
                        data['id'] = row[unique_id]
                    data['key'] = cf
                    if cf_value.startswith('$'):
                        cf_value = cf_value[1:]
                        data['value'] = row[cf_value]
                   
                    if debug or dry_run:
                        print('\tPayload: %s' % data)

                    if(dry_run == False):
                        response = device42_api._put_cf(data, cf_endpoint)
                        print('\tPut:\t%s\tResponse: %s' % (cf_endpoint,response))


def main():
    if use_bulk_fields:
        module_bulk_field()
    else:
        module_normal()

    
if __name__ == '__main__':
    main()
        