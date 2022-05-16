from Controller import Controller
from UnifiAPI import UnifiAPI
import requests
import json

class Unifi:

    def __init__(self, host='', api_user='', api_key='', port=8443):
        self.controller = Controller(host, api_user, api_key, port)
        self.session = requests.Session()
        self._active_site = None
        self._active_device = None

    @property
    def active_site(self):
        if not self._active_site:
            return 'No Site Selected'
        else:
            return self._active_site

    @active_site.setter
    def active_site(self, site):
        self._active_site = site

    @property
    def active_device(self):
        if not self._active_site:
            return 'No Device Selected'
        elif not self._active_site.devices:
            return 'Site is empty!'
        elif not self._active_device:
            return 'No Device Selected'
        else:
            return self._active_device

    @active_device.setter
    def active_device(self, device):
        self.active_device = device

    '''
        Meant to set active_site and active_device during runtime
    '''
    def select_site(self, num=-1):
        if num == -1:

            self.controller.print_sites()
            waiting = 1
            while(waiting):
                try:
                    num = int(input('Select a site from the list: '))
                    waiting = 0
                    self._active_device = None
                except:
                    pass
            for site in self.controller.sites:
                if num == site.num:
                    self._active_site = site
        elif num != -1:
            for site in self.controller.sites:
                if int(num) == site.num:
                    self._active_site = site
                    self.get_devices()


    def select_device(self, num=-1):
        if not self._active_site:
            print("Please select a site first.")
            return
        if num==-1:
            if not self._active_site.devices:
                print("There are no devices to choose from. ")
                return
            else:
                self._active_site.print_devices()
                waiting = 1
                while (waiting):
                    try:
                        num = int(input('Select a device from the list: '))
                        waiting = 0
                    except:
                        pass
                for device in self._active_site.devices:
                    if num == device.num:
                        self._active_device = device
        elif num != -1:
            for device in self._active_site.devices:
                    if int(num) == device.num:
                        self._active_device = device

    '''
        CALLS TO LOGIN/LOGOUT
    '''
    def login(self):
        print('Trying login...')
        login_response = UnifiAPI(self, 'login', json_dict={'username':self.controller.api_user,'password':self.controller.api_key})()
        if login_response == 'api.err.Invalid':
            print('Login unsuccessful. Please try again')
            print(login_response)


    def logout(self):
        print('Called Logout')
        logout_response = UnifiAPI(self, 'logout', json_dict={'doesnt matter':'garbage'})()
        print(logout_response)


    '''
        CALLS THAT AUTO-POPULATE ACTIVE OBJECTS WITH THEIR RESPONSE
    '''
    def get_controller_name(self):
        ''' Gets controller name using 'default' site...which I hope always exists '''
        self.controller.name = UnifiAPI(self, '/api/s/default/stat/sysinfo')()[0]['name']

    def get_sites(self):
        print('Getting Sites')
        self.controller.add_to_sites(UnifiAPI(self, 'self/sites')())

    def get_devices(self):
        print('Getting Devices in [{site}]'.format(site=self._active_site))
        devices = UnifiAPI(self, '/v2/api/site/{site}/device'.format(site=self._active_site.short_name)).v2_call()['network_devices']
        self._active_site.devices = devices


    '''
        CALLS THAT GET INFORMATION ABOUT ACTIVE SELECTIONS
    '''
    def get_controller_info(self):
        ''' Provides completely useless information '''
        print('Getting Controller Info: ')
        controller_info = UnifiAPI(self, 'self')()
        print(json.dumps(controller_info, indent=4))

    def get_topology(self):
        print('Getting {site} topology: '.format(site=self._active_site.name))
        topology = UnifiAPI(self, '/v2/api/site/{site}/topology'.format(site=self._active_site.short_name)).v2_call()
        mac_name=[]
        for device in topology['vertices']:
            if device['type'] == 'DEVICE':
                mac_name.append(
                    {'mac':device['mac'], 'name':device['name']}
                )
        for k in mac_name:
            for device in topology['edges']:
                if k['mac'] == device['downlinkMac']:
                    print ('Device: ' + k['name'], '-- Uplink to port #' + str(device['uplinkPortNumber']), 'on', device['uplinkMac'])
                    print('-'*20)


    def get_wifi(self):
        wifis = UnifiAPI(self, '/v2/api/site/{site}/wlan/enriched-configuration'.format(site=self._active_site.short_name)).v2_call()
        count = 1
        for wifi in wifis:
            if wifi['configuration']['security'] == 'open':
                print(count, '--\tSSID:', wifi['configuration']['name'], '\n\tPwd: [No Password]' '\n')
            else:
                print(count, '--\tSSID:', wifi['configuration']['name'], '\n\tPwd:', wifi['configuration']['x_passphrase'], '\n')
            count+=1


    '''
        CALLS THAT SEND COMMANDS TO ACTIVE DEVICE
    '''
    def set_locate(self):
        print('Locating Device...')
        if not self._active_device:
            print('Pick a device first. ')
            input()
            return
        else:
            endpoint = '/api/s/{site}/cmd/devmgr'.format(site=self._active_site.short_name)
            json_dict = {
                "mac":self._active_device.mac,
                "cmd":"set-locate"
                }
            UnifiAPI(self, endpoint, json_dict=json_dict)()

    def unset_locate(self):
        print('Locating Device...')
        endpoint = '/api/s/{site}/cmd/devmgr'.format(site=self._active_site.short_name)
        json_dict = {
            "mac":self._active_device.mac,
            "cmd":"unset-locate"
            }
        UnifiAPI(self, endpoint, json_dict=json_dict)()
