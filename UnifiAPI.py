import requests
import Controller

''' disables insecure requests warnings '''
requests.packages.urllib3.disable_warnings()

class UnifiAPI:

    def __init__(self, meta, endpoint, path_arg='', json_dict=''):
        self.controller = meta.controller
        self.session = meta.session
        self.endpoint = endpoint
        self.path_arg = path_arg
        self.json_dict = json_dict

    def build_url(self):
        endpoint = self.endpoint if self.endpoint.startswith('/') else '/api/' + self.endpoint

        return 'https://{host}:{port}{endpoint}'.format(
            host=self.controller.host,
            port=self.controller.port,
            endpoint=endpoint
            )

    def __call__(self):
        controller = self.controller
        sesh = self.session
        method = "POST" if self.json_dict else "GET"
        req  = requests.Request(method, self.build_url(), json=self.json_dict)
        resp = sesh.send(sesh.prepare_request(req), verify=False)

        if resp.ok:
            response = resp.json()
            if 'meta' in response and response['meta']['rc'] != 'ok':
                print('API Call Failed' + response['meta']['msg'])
                print(response['meta']['msg'])
            return response['data']
        else:
            print('{}: {}: {}: {}'.format(resp.status_code, resp.reason, resp.text, resp.request.url))

    def v2_call(self):
        controller = self.controller
        sesh = self.session
        method = "POST" if self.json_dict else "GET"
        req  = requests.Request(method, self.build_url(), json=self.json_dict)
        resp = sesh.send(sesh.prepare_request(req), verify=False)

        if resp.ok:
            response = resp.json()
            return response
        else:
            print('{}: {}: {}: {}'.format(resp.status_code, resp.reason, resp.text, resp.request.url))
