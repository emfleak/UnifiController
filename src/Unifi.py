from Controller import Controller
from UnifiAPI import UnifiAPI
import requests
import json
import time
import ast
try:
    import paramiko
except:
    print('[WARNING] - paramiko not loaded, only api functionality will be available.')

class Unifi:

    def __init__(self, host='', api_user='', api_key='', ssh_user='', ssh_pass='',port=8443):
        self.controller = Controller(host, api_user, api_key, port)
        self.session = requests.Session()
        self._active_site = None
        self._active_device = None
        try:
            self.ssh = paramiko.SSHClient()
            self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.ssh.connect(host, username=ssh_user, key_filename=ssh_pass)
            self.base_cmd = '''mongo --port 27117 ace --eval '''
        except:
            print("SSH Connection Failed")
        self.ssh_user = ssh_user
        self.ssh_pass = ssh_pass

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
        self._active_device = device

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
        print('Logging in...')
        login_response = UnifiAPI(self, 'login', json_dict={'username':self.controller.api_user,'password':self.controller.api_key})()
        if login_response != []:
            print('Login unsuccessful. Please try again')
            print(login_response)


    def logout(self):
        print('Logging out...')
        logout_response = UnifiAPI(self, 'logout', json_dict={'doesnt matter':'garbage'})()



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
        #print('Getting Devices in [{site}]'.format(site=self._active_site))
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

    def get_vlans(self):
        print('Getting VLANs for {site}'.format(site=self._active_site.name))
        networks = UnifiAPI(self, '/api/s/{site}/rest/networkconf'.format(site=self._active_site.short_name))()
        ##print(json.dumps(network_conf, indent=4))
        vlans = []

        for network in networks:
            if network['purpose'] == 'vlan-only':
                vlans.append({'name':network['name'], 'vlan-id':network['vlan']})
        return vlans



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

    def get_switch_stats(self):
        switch_stats = UnifiAPI(self, '/api/s/{site}/stat/widget/switch-stats'.format(site=self._active_site.short_name))()
        return switch_stats

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

    # COMMANDS THAT DO DAMAGE
    def delete_site(self):
        while(True):
            confirm = input('Are you sure you want to delete {site}?(Y/n) '.format(site=self._active_site.name))
            if confirm.lower() in ['y','yes']:
                json_dict = {'cmd':'delete-site','site':self._active_site.site_id}
                deleted = UnifiAPI(self, '/api/s/{site}/cmd/sitemgr'.format(site=self._active_site.short_name), json_dict=json_dict)()
                print(deleted)

                print('Refreshing sites....May lose some details')
                self.controller.sites = []
                self.get_sites()
                return
            elif confirm.lower() in ['n','no']:
                print('Cancelled. No changes made.')
                input('Press [enter] to continue.')
                return

    def add_site(self, site_name):
        json_dict = {'desc':site_name, 'cmd':'add-site'}
        response = UnifiAPI(self, '/api/s/default/cmd/sitemgr', json_dict=json_dict)()
        print('Refreshing sites....May lose some details')
        self.controller.sites = []
        self.get_sites()


    # START SSH METHODS
    def find_site_by_mac(self, mac):

        # Setup command. Custom mongo command string that searches the Unifi Controller's 'ace' db by device MAC and returns the siteID
        command_part1 = '''"printjson(db.device.findOne({'mac':\'''' + mac
        command_part2 = ''''},{_id:0,site_id:1,name:1}))"'''
        command = self.base_cmd + command_part1 + command_part2

        # Send/Execute command and get siteID:
        stdin_, stdout_, stderr_ = self.ssh.exec_command(command)
        print("Gathering site information...")
        time.sleep(1)
        output = str(stdout_.read()).split('\\n')

        # Checks output of initial search for the MAC address. If controller returns null, then nothing was found.
        if str(output[2]) == "null":
            print("Device not found")
            wait()
            return 1
        try:
            k = ast.literal_eval(output[2]) #converts db query result into a literal python dictionary type
            site_id = k['site_id']
        except:
            print("Controller returned something unexpected. Please submit a bug report.")
            print(output)


        # Setup command to get Site Name from siteId
        command = '''mongo --port 27117 ace --eval "db.site.find({_id:ObjectId(\'''' + site_id + '''\')},{_id:0,desc:1}).forEach(printjson)" | grep desc '''

        # Send command to return Unifi Site Name
        stdin_, stdout_, stderr_ = self.ssh.exec_command(command)
        # Wait for command to complete
        time.sleep(1)

        output = str(stdout_.read()).split('"')
        site_name = output[3]
        looking = 1
        for site in self.controller.sites:
            if site_name == site.name:
                self._active_site = site
                self.get_devices()
                for device in self._active_site.devices:
                    if mac == device.mac:
                        self._active_device = device
                looking = 0
        if looking:
            print("Device was not found.")
