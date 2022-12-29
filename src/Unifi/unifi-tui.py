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
    8 : 'Controller Queries',
    9 : 'Switch Stats',
    10 : 'Get Site VLANs',
    11 : 'Show SSH Creds',
    12 : 'Adopt Selected Device',
    13 : 'Show Adoptable Devices',
    14 : 'Enable SNMP',
    0 : 'Exit'
}

api_options = {
    1 : 'Start blinking',
    2 : 'Delete site',
    3 : 'Delete device',
    0 : 'Back to Main Menu'
}

controller_queries = {
    1 : 'Switches that are getting full',
    2 : 'Switches using more than 90% of their PoE capacity',
    3 : 'Offline Devices w/ Total WAP & Switch Count',
    4 : 'Sites with no devices',
    5 : 'Offline Devices',
    0 : 'Back to Main Menu'
}

def print_selections(ui):
    print('SITE\t --', ui.active_site, '\nDEVICE\t --', ui.active_device, '\n')

def print_selections_detailed(ui):
    print('SITE\t --', ui.active_site, '\nDEVICE\t --', ui.active_device)
    for prop in ui.active_device.props.keys():
        if prop in ['mac','type','model','ip', 'version', 'state', 'adopted']:
            if prop == 'version':
                print(' |'+str(prop).upper() + '--', str(ui.active_device.props[prop]))
            else:
                print(' |'+str(prop).upper() + '\t --', str(ui.active_device.props[prop]))
    if ui.active_device.props.__contains__('uplink'):
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

def print_controller_menu(ui):
    os.system('clear')
    print('Controller Query Menu : {name}\n'.format(name=ui.controller.name))
    for k in controller_queries:
        print('\t', k, '--', controller_queries[k])
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

        option = input('Make a selection: ')
        try:
            option = int(option)
        except:
            option = option.split(' ')
            print(option)
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
                    continue
                if api_option == 1:
                    if ui.active_device != 'No Device Selected':
                        ui.set_locate()
                        input('Press Enter to stop locating')
                        ui.unset_locate()
                    else:
                        print('Select device first.')
                        wait()
                elif api_option == 2:
                    ui.delete_site()
                elif api_option == 3:
                    ui.delete_device()
                    wait()
                elif api_option == 0:
                    in_api_menu = 0

        elif option == 6:
            if ui.active_site == 'No Site Selected':
                print('Select a site first.')
                wait()
                continue
            ui.get_topology()
            wait()

        elif option == 7:
            ui.get_wifi()
            wait()
        elif option == 8:
            in_controller_menu = 1
            while(in_controller_menu):
                print_controller_menu(ui)
                try:
                    query_option = int(input('Make a selection: '))
                except:
                    print('Wrong input. Please enter a number.')

                if query_option == 1:

                    ''' switches that are getting full '''
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


                elif query_option == 2:
                    ''' Switches that are using too much PoE power '''
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

                elif query_option == 3:
                    ''' Offline Devices w/ Total WAP & Switch Count '''
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

                elif query_option == 4:
                    empty_sites = []
                    print('please wait...')
                    for site in ui.controller.sites:
                        ui.select_site(site.num)
                        if len(site.devices)<=0:
                            empty_sites.append(site.name)
                    for site in empty_sites:
                        print(site)
                    wait()

                elif query_option == 5:
                    ''' Sites with devices offline '''
                    result = {}
                    for site in ui.controller.sites:
                        count = 0
                        found = False
                        ui.select_site(site.num)
                        offline_devices = []
                        for device in site.devices:
                            if device.props['state'] == 0:
                                offline_devices.append(device)
                                found = True
                        if found:
                            print(site.name,':')
                            for k in offline_devices:
                                print('\t',k,'['+k.mac+']')
                            print()
                    # for k in result.keys():
                    #     for j in result[k]:
                    #         print(k, '--\n\t', j.name, '\n\t', j.mac)
                    wait()
                elif query_option == 0:
                    in_controller_menu = 0

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

        elif option == 10:
            vlans = ui.get_vlans()
            for vlan in vlans:
                print(vlan['vlan-id'] + ' -- ' + vlan['name'])
                print()
            wait()

        elif option == 11:
            creds = ui.get_ssh_info()
            print('username: ' + str(creds[0]) + '\npassword: ' + str(creds[1]))
            wait()

        elif option == 12:
            print(ui.adopt_device())
            wait()

        elif option == 13:
            ui.get_devices_for_adoption()

        elif option == 14:
            val = -1
            command = input('enable/disable: ').lower()
            if command=='enable': 
                username = input("username: ")
                password = input("password: ")
                ui.snmp(command, username, password)
                wait()
                val = 1
            elif command=='disable':
                ui.snmp(command)
                wait()
                val = 1
            return val

        elif option == 0:
            ui.logout()
            exit()

        elif option[0] == 'add':
            if option[1] == 'site':
                site_name = option[2]
            ui.add_site(site_name)
            wait()

if __name__=='__main__':
    main()
