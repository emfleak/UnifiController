from Unifi import Unifi
import json
import csv
import os
from time import sleep

menu_options = {
    1 : 'Select Site',
    2 : 'Select Device',
    3 : 'Search MAC',
    4 : 'Show device info',
    5 : 'Device API Actions',
    6 : 'Get Site Topology',
    7 : 'View Wifi Settings',
    9 : 'Switch Stats',
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

        elif option == 6968:
            total_device_count = 0
            total_wap_count = 0
            total_switch_count = 0
            total_offline_count = 0
            for site in ui.controller.sites:
                ui.select_site(site.num)
                sub_wap_count = 0
                sub_switch_count = 0
                sub_device_count = 0
                sub_offline_count = 0
                #print('Site: ' + site.name)
                for device in site.devices:

                    ui.select_device(device.num)
                    if device.props['state'] == 0:
                        print("Device Offline: " + device.name + '[' + device.mac + '] at ' + device.site.name)
                        sub_offline_count+=1
                    if device.type == 'usw':
                        sub_switch_count+=1
                    if device.type == 'uap':
                        sub_wap_count+=1
                    sub_device_count+=1

                    #print(device.type,' -- ', device.props['model'], ' -- ', device.name)

                # print('WAP: ' + str(sub_wap_count))
                # print('SWITCH: ' + str(sub_switch_count))
                # print('Site Total: ' + str(sub_device_count))
                total_wap_count+=sub_wap_count
                total_switch_count+=sub_switch_count
                total_device_count+=sub_device_count
                total_offline_count+=sub_offline_count

            print('Total WAPs: ' + str(total_wap_count))
            print('Total switches: ' + str(total_switch_count))
            print('Devices Offline: ' + str(total_offline_count))
            print('Total Devices: ' + str(total_device_count))
            ui.active_site = None
            ui.active_device = None
            wait()

        elif option == 6969:
            full_switches = []
            last_active_site = ui.active_site
            for site in ui.controller.sites:
                ui.select_site(site.num)

                if len(ui.active_site.devices) != 0:
                    switches = ui.get_switch_stats()
                    for switch in switches:
                        if switch['total_max_power'] - switch['current_power'] <= 50 and switch['total_max_power'] > 50:
                            for device in ui.active_site.devices:
                                if device.mac == switch['mac']:
                                    full_switches.append({'site':device.site.name,'name':device.name,'total_ports':switch['total_ports'],'ports_remaining':str(switch['total_ports']-switch['used_ports']), 'max_poe':switch['total_max_power'],'poe':switch['current_power']})

            for switch in full_switches:
                print(json.dumps(switch, indent=2))
            wait()
            ui.active_site = None

        elif option == 8:
            full_switches = []
            last_active_site = ui.active_site
            for site in ui.controller.sites:
                ui.select_site(site.num)

                if len(ui.active_site.devices) != 0:
                    switches = ui.get_switch_stats()
                    for switch in switches:
                        if switch['total_ports']-switch['used_ports'] <= 10 and switch['total_ports'] >= 16:
                            for device in ui.active_site.devices:
                                if device.mac == switch['mac']:
                                    full_switches.append({'site':device.site.name,'name':device.name,'total_ports':switch['total_ports'],'ports_remaining':str(switch['total_ports']-switch['used_ports'])})

            for switch in full_switches:
                print(json.dumps(switch, indent=2))
            wait()
            ui.active_site = None

        elif option == 9:

            switch_stats = ui.get_switch_stats()
            for switch in switch_stats:
                for device in ui.active_site.devices:
                    if switch['mac'] == device.mac:
                        print('Name: ' + device.name)
                        for prop in switch:
                            if prop in ['mac','current_power','total_max_power','total_ports','used_ports']:
                                device.props.update({prop:switch[prop]})
                                print(prop + ':', str(switch[prop]))

                print()
            wait()

        elif option == 0:
            ui.logout()
            exit()


if __name__=='__main__':
    main()
