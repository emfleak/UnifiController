from Unifi import Unifi
import os
from getpass import getpass

commands = ['show','select','get','set','quit','help']
show_commands = ['sites','devices','site','device','selections']
select_commands = ['site','device']
get_commands = ['site','device','wifi']

def print_help():
    print('Unifi Controller Command Line API Interface\n\n' +
            'Available commands: ')
    for k in commands:
        print ('\t'+k)

        if k == 'show':
            for j in show_commands:
                print('\t\t'+j)

        if k == 'select':
            for j in select_commands:
                print('\t\t'+j
                )
        if k == 'get':
            for j in get_commands:
                print('\t\t'+j)

def print_selections(ui):
    print('Site:\t', ui.active_site, '\nDevice:\t', ui.active_device, '\n')

def print_menu(ui):
    print('Unifi Menu : {name}\n'.format(name=ui.controller.name))
    for k in menu_options:
        print('\t', k, '--', menu_options[k])
    print()

def wait():
    input('Press [enter] to continue...\n')

def wrong():
    print('Invalid command. Type ? for help.\n')

def incomplete():
    print('Incomplete command. Type ? for help')

def no_site():
    print('select a site first.\n')


def main():
    host = 'unifi.biztec.us'
    # print('login --')
    # user = input('\tUsername: ')
    # pwd = getpass('\tPassword: ')
    user = 'api_user'
    pwd = 'Emerson123!'
    ui = Unifi(host, user, pwd)
    ui.login()
    try:
        ui.get_controller_name()
    except:
        print('no controller')
    try:
        ui.get_sites()
    except:
        print('no sites')
    while(True):

        command = input('> ').split(' ')
        size = len(command)
        #print(size, command)
        if command[0] == '':
            continue

        # if command[0] == 'login':
        #     host = 'unifi.biztec.us'
        #     #host = input('hostname: ')
        #     user = input('username: ')
        #     pwd = getpass()
        #     ui = Unifi(host, user, pwd)
        #     ui.get_sites()

        elif command[0] == 'show':
            ''' SHOW DIRECTIVE '''

            if command[1] == 'sites':
                ''' SHOW ALL SITES ON CONTROLLER '''
                ui.controller.print_sites()

            elif command[1] == 'site':
                ''' SHOW SELECTED SITE '''
                print(ui.active_site)


            elif command[1] == 'devices':
                ''' SHOW ALL DEVICES IN SELECTED SITE '''
                try:
                    ui.active_site.print_devices()
                except:
                    print(ui.active_site)

            elif command[1] == 'device':
                ''' SHOW SELECTED DEVICE '''
                print(ui.active_device)

            elif command[1] == 'selections':
                ''' SHOW SITE & DEVICE SELECTIONS '''
                print_selections(ui)

            else:
                wrong()
                continue


        elif command[0] == 'select':
            ''' SELECT DIRECTIVE '''

            if command[1] == 'site':
                ''' SELECT SITE BY NUMBER '''
                if size != 3:
                    wrong()
                    continue
                ui.select_site(num=command[2])


            elif command[1] == 'device':
                ''' SELECT DEVICE BY TUI OR NUMBER '''

                if size == 2:
                    ui.select_device()
                elif size == 3:
                    ui.select_device(num=command[2])
                else:
                    wrong()
                    continue

            else:
                wrong()
                continue

        elif command[0] == 'get':
            ''' GET DIRECTIVE '''
            if size == 1:
                wrong()
                continue

            if command[1] == 'device':
                ''' GET DEVICE PROPERTIES '''
                if size >= 3:

                    if command[2] == 'info':
                        ui._active_device.display()

                else:
                    incomplete()
                    continue

            if command[1] == 'wifi':
                wrong() if size > 2 else ui.get_wifi()

            if command[1] == 'topology':
                wrong() if size > 2 else ui.get_topology()

        elif command[0] == 'set':
            ''' SET DIRECTIVE '''
            if size == 1:
                wrong()
                continue



        elif command[0] in ['help', '?']:
            print_help()

        #''' EXIT '''
        elif command[0] in ['exit','quit','q']:
            ui.logout()
            exit()

        else:
            wrong()


if __name__=='__main__':
    main()
