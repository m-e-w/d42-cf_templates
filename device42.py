import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import base64
import json


class Device42Api:
    def __init__(self, config, options):
        self.username = config['username']
        self.password = config['password']
        self.host = config['host']
        self.debug = options['debug']
        self.dry_run = options['dry_run']

    def _get(self, data, url):
        params = data
        r = requests.get(url, params=params,auth=HTTPBasicAuth(self.username, self.password), verify=False)
        return r

    def _post(self, data, url):
        payload = data
        r = requests.post(url, payload, auth=HTTPBasicAuth(self.username, self.password), verify=False)
        return r

    def _put(self, data, url):
        payload = data
        r = requests.put(url, payload, auth=HTTPBasicAuth(self.username, self.password), verify=False)
        return r

    def _query(self,query):
        url = 'https://%s/services/data/v1.0/query/' % self.host
        data = {"query":query, "output_type":"json"}
        return self._get(data, url).json()

    def _get_doql(self, saved_doql):
        url = 'https://%s/services/data/v1.0/query/' % self.host
        data = {"saved_query_name":saved_doql, "output_type":"json"}
        return self._get(data, url).json()

    def _post_appcomp(self, data):
        url = 'https://%s/api/1.0/appcomps/' % self.host
        return self._post(data, url).json()
    
    def _post_serviceinstance(self, data): 
        url = 'https://%s/api/2.0/service_instances/' % self.host
        return self._post(data, url).json()

    def _put_cf(self, data, endpoint):
        url  = 'https://%s%s' % (self.host, endpoint)
        return self._put(data, url).json()

 
