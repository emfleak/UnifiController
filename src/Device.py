import Site
import json

class Device:
    def __init__(self, mac, type='', model='', site='', name='', version='', num=0, props={}):
        self.num = num
        self.mac = mac
        self.name = name
        self.type = type
        self.model = model
        self.site = site
        self.version = version
        self.props = props

    def __str__(self):
        if not self.name:
            return self.mac
        else:
            return self.name

    def display(self):
        print(str(self.num) + ' --')
        for prop in self.props:
            if prop in ['name', 'mac', 'type', 'model', 'version', 'ip',  'uplink', 'uptime']:
                if prop in ['uplink']:
                    try:
                        print('\tUplink: port #' + str(self.props[prop]['port_idx']) + ' to ' + self.props[prop]['uplink_device_name'] + ' [' + self.props[prop]['uplink_mac'] + '] on port #' + str(self.props[prop]['uplink_remote_port']))
                    except:
                        print('\tUplink: port #' + str(self.props[prop]['port_idx']) + ' (not uplinked to a unifi device)')
                    else:
                        print('\tUplink: port #' + str(self.props[prop]['ap_mac']) + ' (not uplinked to a unifi device)')
                else:
                    print('\t' + str(prop) + ': ' + str(self.props[prop]))

    def display_short(self):
        print(str(self.num) + ' --\tName: ' + self.name + '\n\tMac: ' + self.mac + '\n\tType: ' + self.type.upper() + '\n\tModel: ' + self.model)

    def get_site_id(self):
        return self.site.site_id

    def is_site(self):
        if self.site == '':
            return False
        else:
            return True
