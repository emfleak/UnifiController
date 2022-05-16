from Unifi import Unifi
import os

commands = ['show','select','get','set','exit','help']
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
    print('Incomplete command. Type "help" for help.\n')
    
def no_site():
    print('select a site first.\n')
    

def main():
    ui = Unifi('unifi.biztec.us', 'api_user', 'Emerson123!')

    ui.login()
    ui.get_controller_name()
    ui.get_sites()

    while(True):
        
        command = input('> ').split(' ')
        size = len(command)
        print(size, command)
        if size == 0:
            continue
            
        if command[0] in commands and size == 1:
            wrong()
            continue
        
        ''' SHOW '''
        if command[0] == 'show':
            
            ''' SITE CONTEXT '''
            if command[1] == 'sites':
                ui.controller.print_sites()
                
            elif command[1] == 'site':
                print(ui.active_site)
                    
            #''' DEVICE CONTEXT '''
            elif command[1] == 'devices':
                try:
                    ui.active_site.print_devices()
                except:
                    print(ui.active_site)
                    
            elif command[1] == 'device':
                
                print(ui.active_device)
            
            elif command[1] == 'selections':
                print_selections(ui)
                print(ui.active_site)
                print(ui.active_device)
            
            else:
                wrong()
                continue
                
        #''' SELECT '''       
        elif command[0] == 'select':
            
            ''' SITE CONTEXT '''
            if command[1] == 'site':
                if size <=2:
                    wrong()
                    continue
                ui.select_site(num=command[2])
            
            #''' DEVICE CONTEXT '''
            elif command[1] == 'device':
                if size<=2:
                    wrong()
                    continue
                ui.select_device(num=command[2])
                
            else:
                wrong()
                continue
                
        elif command[0] == 'get':
            if size == 1:
                wrong()
                continue
            if command[1] == 'wifi':
                print(ui.get_wifi())
                
                
        elif command[0] in ['help','?', 'wtf']:
            print_help()
            
        #''' EXIT '''
        elif command[0] in ['exit','quit','q']:
            ui.logout()
            exit()
        
        else:
            wrong()


if __name__=='__main__':
    main()
