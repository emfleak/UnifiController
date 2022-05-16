import Controller
from Device import Device

class Site:

    def __init__(self, name='', site_id='', short_name='', num=0):
        self.num = num
        self.name = name
        self.site_id = site_id
        self.short_name = short_name
        self._devices = []
        self._wifis = []

    @property
    def devices(self):
        return self._devices

    @devices.setter
    def devices(self, devices):
        if self.devices == []:
            num = 0
        else:
            print ('Already Got Devices, skipping')
            return
        for device in devices:
            props = {}
            for prop in device:
                props.update({prop:device[prop]})
            try:
                self.devices.append(Device(device['mac'], device['type'], name=device['name'], site=self, num=num, props=props))
            except:
                self.devices.append(Device(device['mac'], device['type'], site=self, num=num, props=props))
            num+=1

    @property
    def wifis(self):
        return self._wifis

    @wifis.setter
    def wifis(self, wifis):
        self.wifis = wifis

    def __str__(self):
        return self.name

    def display(self):
        print(str(self.num) + ' --\n\tName: ' + self.name + '\n\tSite ID: ' + self.site_id + '\n\tShort Name: ' + self.short_name)

    ''' THIS CAN PROBABLY BE @devices.setter BUT I HAVENT TRIED '''
    def add_to_devices(self, devices):
        if self.devices == []:
            num = 0
        else:
            print ('Already Got Devices, skipping')
            return
        for device in devices:
            try:
                self.devices.append(Device(device['mac'], device['type'], name=device['name'], model=device['model'], site=self, num=num))
            except:
                self.devices.append(Device(device['mac'], device['type'], site=self, num=num))
            num+=1

    def print_devices(self):
        for device in self.devices:
            device.display_short()
            print()

    def search_device(self, mac):
        for device in self.devices:
            if mac == device.mac:
                return device.name
