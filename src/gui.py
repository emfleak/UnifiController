import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from Unifi import Unifi

root=tk.Tk()
root.title('Unifi Controller')
root.geometry('350x500')


def populate_sites_listbox():
    for site in ui.controller.sites:
        sites_listbox.insert(site.num, site.name)

def list_device_btn_clicked():

    i = sites_listbox.curselection()
    site = sites_listbox.get(i)
    for k in ui.controller.sites:
        if site == k.name:
            ui.select_site(k.num)
    for device in ui.active_site.devices:
        devices_listbox.insert(device.num, device.name)

def login_btn_clicked():
    global ui
    ui = Unifi('unifi.biztec.us', username.get(), password.get())
    ui.login()
    ui.get_controller_name()
    ui.get_sites()
    populate_sites_listbox()
    login.destroy()
    # msg = 'Logged into ' + ui.controller.host
    # msg = '\n'
    # for site in ui.controller.sites:
    #     msg+=site.name
    #     msg+='\n'
    #showinfo(title='Info', message=msg)

# Login Frame
login = ttk.Frame(root)
login.pack(padx=10,pady=10, fill='x', expand=True)

# Site & Device Frame
info = ttk.Frame(root)
info.pack(padx=10, pady=10, fill='x', expand=True)

# Username
username = tk.StringVar(login, value='api_user')
username_label = ttk.Label(login, text="User: ")
username_label.pack(fill='x', expand=True)
username_box = ttk.Entry(login, textvariable=username)
username_box.pack(fill='x', expand=True)
username_box.focus()

# password
password = tk.StringVar(login, value='Emerson123!')
password_label = ttk.Label(login, text="Password: ")
password_label.pack(fill='x', expand=True)
password_box = ttk.Entry(login, textvariable=password, show='*')
password_box.pack(fill='x', expand=True)

# Login Button
login_btn = tk.Button(login, text='Login',command=login_btn_clicked)
login_btn.pack(fill='x', expand=True, pady=10)

# Sites Label
sites_label = ttk.Label(info, text='Sites: ')
sites_label.pack(fill='x', expand=True)
# Sites listbox
sites_listbox = tk.Listbox(info)
sites_listbox.pack(fill='x', expand=True)

#list_sites_btn = tk.Button(root, text='List Sites', width=10,height=5,command=site_list_box)

# Devices Button
list_device_btn = tk.Button(info, text='List Devices', command=list_device_btn_clicked)
list_device_btn.pack(fill='x', expand=True, padx=10)

# Devices listbox
devices_label = ttk.Label(info, text="Devices: ")
devices_label.pack(fill='x', expand=True)
devices_listbox = tk.Listbox(info)
devices_listbox.pack(fill='x', expand=True)

root.mainloop()
