import Site

class Device:
    def __init__(self, mac, type='', model='', site='', name='', num=0):
        self.num = num
        self.mac = mac
        self.name = name
        self.type = type
        self.model = model
        self.site = site

    def __str__(self):
        if not self.name:
            return self.mac
        else:
            return self.name

    def display(self):
        print(str(self.num) + ' --\n\t' + 'Name: ' + self.name + '\n\tMac: ' + self.mac + '\n\tType: ' + self.type)

    def get_site_id(self):
        return self.site.site_id

    def is_site(self):
        if self.site == '':
            return False
        else:
            return True
