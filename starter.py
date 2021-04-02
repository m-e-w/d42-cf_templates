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

def main():
    
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
                    data = templates[template]['custom_fields'][cf]
                    data['id'] = row[unique_id]
                    data['key'] = cf

                    print('\nPut: %s' % cf_endpoint)
                    print('\tPayload: %s' % data)

                    if(dry_run):
                        print('\tResponse: N/A - Dry Run') 
                    else:
                        response = device42_api._put_cf(data, cf_endpoint)
                        print('\tResponse: %s' % response)
    
if __name__ == '__main__':
    main()
        