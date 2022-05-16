from Unifi import Unifi
import os

menu_options = {
    1 : 'Select Site',
    2 : 'Select Device',
    3 : 'Blink Device',
    4 : 'Stop Blinking Device',
    6 : 'Get Site Topology',
    7 : 'View Wifi Settings'
}

def print_selections(ui):
    print('Site:\t', ui.active_site, '\nDevice:\t', ui.active_device, '\n')
def print_menu(ui):
    print('Unifi Menu : {name}\n'.format(name=ui.controller.name))
    for k in menu_options:
        print('\t', k, '--', menu_options[k])
    print()
def wait():
    input('Press [enter] to continue...')
def print_options():
    pass

def main():
    ui = Unifi('unifi.biztec.us', 'api_user', 'Emerson123!')

    ui.login()
    ui.get_controller_name()
    ui.get_sites()

    while(True):
        os.system('clear')
        print_menu(ui)
        print_selections(ui)

        option = ''
        try:
            option = int(input('Make a selection: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
            ui.select_site()
            ui.get_devices()
        elif option == 2:
            ui.select_device()
        elif option == 3:
            ui.set_locate()
        elif option == 4:
            ui.unset_locate()
        elif option == 5:
            pass
        elif option == 6:
            ui.get_topology()
            wait()
        elif option == 7:
            ui.get_wifi()
            wait()
        elif option == 8:
            ui._active_device.display()
            wait()
        elif option == 0:
            ui.logout()
            exit()


if __name__=='__main__':
    main()
