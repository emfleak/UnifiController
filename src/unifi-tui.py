from Unifi import Unifi
import os

menu_options = {
    1 : 'Select Site',
    2 : 'Select Device',
    3 : 'Search MAC',
    4 : 'Show device info',
    5 : 'Device API Actions',
    6 : 'Get Site Topology',
    7 : 'View Wifi Settings',
    0 : 'Exit'
}

api_options = {
    1 : 'Start blinking',
    0 : 'Back to Main Menu'
}

def print_selections(ui):
    print('SITE\t --', ui.active_site, '\nDEVICE\t --', ui.active_device, '\n')
def print_selections_detailed(ui):
    print('SITE\t --', ui.active_site, '\nDEVICE\t --', ui.active_device)
    for prop in ui.active_device.props.keys():
        if prop in ['mac','type','model','ip', 'version']:
            if prop == 'version':
                print(' |'+str(prop).upper() + '--', str(ui.active_device.props[prop]))
            else:
                print(' |'+str(prop).upper() + '\t --', str(ui.active_device.props[prop]))
    print(' |UPLINK -- ' + ui.active_device.get_prop('uplink'))
    print()
def print_menu(ui):
    os.system('clear')
    print('Unifi Menu : {name}\n'.format(name=ui.controller.name))
    for k in menu_options:
        print('\t', k, '--', menu_options[k])
    print()
def print_api_menu(ui):
    os.system('clear')
    print('API Menu : {name}\n'.format(name=ui.controller.name))
    for k in api_options:
        print('\t', k, '--', api_options[k])
    print()
def wait():
    input('Press [enter] to continue...')
def print_options():
    pass

def main():
    ui = Unifi('unifi.biztec.us', 'api_user', 'Emerson123!', 'ubuntu', '/Users/evan/.ssh/Biztec-UniFi.pem')

    ui.login()
    ui.get_controller_name()
    ui.get_sites()

    while(True):

        print_menu(ui)
        if ui.active_device == 'No Device Selected' or ui.active_device == 'Site is empty!':
            print_selections(ui)
        else:
            print_selections_detailed(ui)

        option = ''
        try:
            option = int(input('Make a selection: '))
        except:
            print('Wrong input. Please enter a number.')
        if option == 1:
            ui.select_site()
            ui.get_devices()

        elif option == 2:
            ui.select_device()

        elif option == 3:
            mac = input("Enter a device mac: ").lower()
            ui.find_site_by_mac(mac)
            wait()

        elif option == 4:
            ui.active_device.display()
            wait()

        elif option == 5:
            in_api_menu = 1
            while(in_api_menu):
                print_api_menu(ui)
                try:
                    api_option = int(input('Make a selection: '))
                except:
                    print('Wrong input. Please enter a number.')
                if api_option == 1:
                    if ui.active_device != 'No Device Selected':
                        ui.set_locate()
                        input('Press Enter to stop locating')
                        ui.unset_locate()
                    else:
                        print('Select device first.')
                        wait()
                elif api_option == 0:
                    in_api_menu = 0

        elif option == 6:
            ui.get_topology()
            wait()

        elif option == 7:
            ui.get_wifi()
            wait()

        elif option == 8:
            ui._active_device.display()
            wait()

        elif option == 9:
            pass

        elif option == 0:
            ui.logout()
            exit()


if __name__=='__main__':
    main()
