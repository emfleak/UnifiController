import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo
from Unifi import Unifi
import json

root=tk.Tk()
root.title('Unifi Controller')
#root.geometry('350x500')
window_width = 700
window_height = 500
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = screen_width/2 - window_width/2
y = screen_height/2 - window_height/2
root.geometry('%dx%d+%d+%d' % (window_width, window_height, x, y))


def populate_sites_listbox():
    for site in ui.controller.sites:
        sites_listbox.insert(site.num, site)

def show_info():
    sites_label.pack(fill='x', expand=True)
    sites_listbox.pack(fill='x', expand=True)
    devices_label.pack(fill='x', expand=True)
    devices_listbox.pack(fill='x', expand=True)

def show_site_info(event=None):
    site_info.config(highlightthickness=1)
    site_info_label.config(text='')
    site_wifi_label.config(text='')
    site_switch_stats_label.config(text='')
    device_info_label.config(text='')
    devices_listbox.delete(0,END)

    i = sites_listbox.curselection()
    site = sites_listbox.get(i)
    for k in ui.controller.sites:
        if site == k.name:
            ui.select_site(k.num)

    site_info_label.config(text=ui.active_site)
    site_wifi_label.config(text=ui.get_wifi(), justify='left')
    switch_stats = ui.get_switch_stats()
    msg = ''
    for switch in switch_stats:
        for prop in switch.keys():
            if prop != 'ports':
                msg+=prop+': '+str(switch[prop])+'\n'
        msg+='\n'
    site_switch_stats_label.config(text=msg, justify='left')


    site_info_label.grid(row=0, column=0, sticky='nw')
    site_wifi_label.grid(row=1, column=0, sticky='w')
    site_switch_stats_label.grid(row=0, column=1, rowspan=100, sticky='s')

    for device in ui.active_site.devices:
        devices_listbox.insert(device.num, device)

def show_dev_info(event=None):
    # Device info Label

    device_info_label.config(text='')
    i = devices_listbox.curselection()
    print(i[0])
    device = devices_listbox.get(i)

    for k in ui.active_site.devices:
        if i[0] == k.num:
            ui.select_device(k.num)
    print('[LOG] - Made it here. Line 45')
    msg = 'Selected Device: \n'
    for prop in ui.active_device.props.keys():
        if prop in ['name', 'mac', 'type', 'model', 'adopted']:
            msg+=prop+':\t'+str(ui.active_device.props[prop])+'\n'
        if prop in ['uplink']:
            msg+=prop+':\t'+str(ui.active_device.get_prop(prop))
    device_info_label.config(text=msg)


    device_info_label.grid(row=0, column=0)

def login_btn_clicked():
    global ui
    ui = Unifi('unifi.biztec.us', username.get(), password.get())
    ui.login()
    ui.get_controller_name()
    ui.get_sites()
    populate_sites_listbox()
    login.destroy()
    show_info()
    sites_listbox.bind("<<ListboxSelect>>", show_site_info)
    devices_listbox.bind("<<ListboxSelect>>", show_dev_info)
    # msg = 'Logged into ' + ui.controller.host
    # msg = '\n'
    # for site in ui.controller.sites:
    #     msg+=site.name
    #     msg+='\n'
    #showinfo(title='Info', message=msg)

# Login Frame
login = tk.Frame(root, highlightthickness=1)
login.grid(row=0,column=0)

# Site selection Frame
site_select = tk.Frame(root)
site_select.grid(row=0,column=0,padx=10,pady=10)

# Device Selection Frame
device_select = tk.Frame(root)
device_select.grid(row=1, column=0, padx=10, pady=10)

# Site Info Frame
site_info = tk.Frame(root, highlightthickness=10)
site_info.grid(row=0,column=1, padx=10, pady=10, sticky='w')

# Device Info Frame
dev_info = tk.Frame(root, highlightthickness=10)
dev_info.grid(row=1, column=1,padx=10,pady=10)

# Username label
username_label = ttk.Label(login, text="User: ")
username_label.grid(row=0, column=0)

# Username Entry Box
username = tk.StringVar(login, value='api_user')
username_box = ttk.Entry(login, textvariable=username)
username_box.grid(row=0, column=1)
username_box.focus()

# password label
password_label = ttk.Label(login, text="Password: ")
password_label.grid(row=1,column=0)

# password entry box
password = tk.StringVar(login, value='Emerson123!')
password_box = ttk.Entry(login, textvariable=password, show='*')
password_box.grid(row=1,column=1)

# Login Button
login_btn = tk.Button(login, text='Login',command=login_btn_clicked)
login_btn.grid(row=2,column=0, columnspan=2, pady=10)

# Sites Label
sites_label = ttk.Label(site_select, text='Sites: ')

# Sites listbox
sites_listbox = tk.Listbox(site_select, exportselection=False)

# Devices label
devices_label = ttk.Label(device_select, text="Devices: ")

# Devices listbox
devices_listbox = tk.Listbox(device_select, exportselection=False)

# Device Info Label
device_info_label = ttk.Label(dev_info)

# Site Info label
site_info_label = tk.Label(site_info)

# Site Wifi Label
site_wifi_label = tk.Label(site_info)

# Switch stats label
site_switch_stats_label = tk.Label(site_info)

root.mainloop()
