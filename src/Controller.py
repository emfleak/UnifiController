from Site import Site

class Controller:

    def __init__(self, host, api_user, api_key, ssh_user='', ssh_pass='',port=8443):
        self.host = host
        self.port = port
        self.api_user = api_user
        self.api_key = api_key
        self.name = ''
        self.sites = []

    def __str__(self):
        return 'Controller\n\tHost: {host}:{port}\n\tUser: {api_user}\n\tKey: {api_key}'.format(host=self.host,port=self.port,api_user=self.api_user,api_key=self.api_key)

    def add_to_sites(self, sites):
        num = 0
        for site in sites:
            exists = 0
            for existing in self.sites:
                if site['name'] == existing.name:
                    print('Already got ' + site['name'])
                    exists = 1

            if not exists:
                self.sites.append(Site(site['desc'], site['_id'], site['name'], num=num))
            num+=1

    def print_sites(self):
        for site in self.sites:
            print(site.num, '--', site.name)
