import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
from Unifi import Unifi

class PageContainer(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.logged_in = 0
        self.title('Unifi')
        self.config(bg='#93B3CC')
        container = tk.Frame(self)

        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=2)
        container.grid_rowconfigure(1, weight=2)
        container.grid_columnconfigure(0, weight=1)

        self.frame = {}
        count = 0
        for F in (LoginPage, MainPage, SiteSummary):
            print(str(count))
            frame = F(container, self)
            self.frame[F] = frame
            frame.grid(row=0, column=0, sticky='nsew')
            count+=1

        self.show_frame(LoginPage)

    def show_frame(self, container):
        if container == MainPage:
            self.geometry('750x520')
        if container == LoginPage:
            self.geometry('280x125')
        frame = self.frame[container]
        frame.tkraise()

class LoginPage(tk.Frame):

    def __init__(self, parent, controller):
        print('made it here')
        tk.Frame.__init__(self, parent, padx=10, pady=10)
        self.controller = controller
        #self.config(bg='#93B3CC')

        # Username label
        username_label = tk.Label(self, text="User: ")
        username_label.grid(row=0, column=0)

        # Username Entry Box
        self.username = tk.StringVar(self, value='api_user')
        username_box = tk.Entry(self, textvariable=self.username)
        username_box.grid(row=0, column=1)
        username_box.focus()

        # password label
        password_label = tk.Label(self, text="Password: ")
        password_label.grid(row=1,column=0)

        # password entry box
        self.password = tk.StringVar(self, value='Emerson123!')
        password_box = tk.Entry(self, textvariable=self.password, show='*')
        password_box.grid(row=1,column=1)

        # Login Button
        login_btn = tk.Button(self, text='Login',command=self.login_btn_clicked)
        login_btn.grid(row=2,column=0, columnspan=2, pady=10)

    def login_btn_clicked(self):
        host = 'unifi.biztec.us'
        user = self.username.get()
        pwd = self.password.get()
        self.controller.ui = Unifi(host, user, pwd)

        login_response = self.controller.ui.login()
        if login_response == 'api.err.Invalid':
            showinfo(message='Login failed, try again.')
        else:
            #self.controller.geometry('400x700')
            self.controller.logged_in=1
            self.controller.frame[MainPage].populate_sites_listbox()
            self.controller.show_frame(MainPage)

class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.config(bg='#93B3CC')
        self.grid_columnconfigure(index=1, weight=3)
        self.controller = controller
        self.frame = {}
        for F in (None, None):
            pass

        options = {'padx': 10, 'pady': 10}
        listbox_options = {
            'bg':'#93B3CC',
            'fg':'black',
            'bd':4,
            'exportselection':False
        }
        self.labelframe_options = {
            'bg':'#93B3CC',
            'fg':'black',
            'bd':4,
        }
        sites_label = tk.Label(self, text='Sites: ', bg='#93B3CC')
        sites_label.grid(row=0, column=0, sticky='sw', **options)

        self.sites_listbox = tk.Listbox(self, **listbox_options)
        self.sites_listbox.bind('<<ListboxSelect>>', self.handle_select_site)
        self.sites_listbox.grid(row=1, column=0, sticky='w', **options)

        self.sites_listbox_scrollbar = tk.Scrollbar(self)

        devices_label = tk.Label(self, text="Devices: ", bg='#93B3CC')
        devices_label.grid(row=2, column=0, sticky='w', **options)

        self.devices_listbox = tk.Listbox(self, **listbox_options)
        self.devices_listbox.bind('<<ListboxSelect>>', self.handle_select_device)
        self.devices_listbox.grid(row=3, column=0, sticky='w', **options)

        device_info_label = tk.Label(self)
        site_info_label = tk.Label(self)
        site_wifi_label = tk.Label(self)
        site_switch_stats_label = tk.Label(self)

        logout_btn = tk.Button(self,text='Logout', command=self.logout, background='#93B3CC').grid(row=4, column = 3)

        self.site_info_labelframe = tk.LabelFrame(self, text='Site Info', **self.labelframe_options)
        self.site_info_labelframe.grid(row=0, column=1, columnspan=2, rowspan=2, sticky='nsew', **options)

        self.device_info_labelframe = tk.LabelFrame(self, text='Device Info', **self.labelframe_options)
        self.device_info_labelframe.grid(row=2, column=1, columnspan=2, rowspan=2, sticky='nsew', **options)

        self.site_summary_btn = tk.Button(self, text="Sites Summary", command=self.handle_site_summary_btn)
        self.site_summary_btn.grid(row=4, column = 2)

    # handler for site_listbox selection
    def handle_select_site(self, event):
        # get index of selected site (curselection returns tuple of multiselection indicies)
        i = self.sites_listbox.curselection()[0]
        # use the index to select Unifi instance's active_site by number select_site(site.num)
        self.controller.ui.select_site(i)
        # refresh other widgets with new site
        self.populate_site_info_labelframe()
        self.populate_devices_listbox()

    # handler for device_listbox selction
    def handle_select_device(self, event):
        # get index of selected site (curselection returns tuple of multiselection indicies)
        i = self.devices_listbox.curselection()[0]
        # use the index to select Unifi instance's active_device by number select_device(device.num)
        self.controller.ui.select_device(i)
        # refresh device info labelframe
        self.populate_device_info_labelframe()

    def handle_site_summary_btn(self):
        self.controller.show_frame(SiteSummary)
        self.controller.frame[SiteSummary].populate_site_summary()

    def populate_sites_listbox(self):
        if self.controller.logged_in:
            self.controller.ui.get_sites()
            for site in self.controller.ui.controller.sites:
                self.sites_listbox.insert(site.num, str(site.num) + ': ' + str(site))

    def populate_devices_listbox(self):
        # delete any previous devices from listbox
        self.devices_listbox.delete(0, 'end')

        # delete any previous device info from device info labelframe
        for widget in self.device_info_labelframe.pack_slaves():
            widget.destroy()

        # iterate through active site devices and insert them into the devices listbox
        for device in self.controller.ui.active_site.devices:
            self.devices_listbox.insert(device.num, str(device.num) + ': ' + str(device))

    def populate_site_info_labelframe(self):
        site = self.controller.ui.active_site
        lf = self.site_info_labelframe
        lf.config(text=site.name)
        self.controller.ui.get_wifi()

        for widget in lf.pack_slaves():
            widget.destroy()

        if len(site.wifis) > 0:
            for wifi in site.wifis:
                tk.Label(lf, text='SSID: '+wifi['configuration']['name'], **self.labelframe_options).pack(anchor='w')
                tk.Label(lf, text='\tSecurity:\t'+wifi['configuration']['security'], **self.labelframe_options).pack(anchor='w')
                if wifi['configuration'].__contains__('x_passphrase'):
                    tk.Label(lf, text='\tPassword: \t'+wifi['configuration']['x_passphrase'], **self.labelframe_options).pack(anchor='w')
                #tk.Label(lf).pack(anchor='w')



    def populate_device_info_labelframe(self):
        device = self.controller.ui.active_device
        lf = self.device_info_labelframe
        lf.config(text=device.name)

        # delete any previous device info from device info labelframe
        for widget in lf.pack_slaves():
            widget.destroy()

        for prop in device.props.keys():
            if prop in ['mac', 'type', 'model', 'adopted', 'state']:
                tk.Label(lf, text=prop+':\t'+str(device.props[prop]), **self.labelframe_options).pack(anchor='w')
            if prop in ['uplink']:
                tk.Label(lf, text=prop+':\t'+str(device.get_prop(prop)), **self.labelframe_options).pack(anchor='sw')

    def logout(self):
        self.controller.ui.logout()
        self.controller.show_frame(LoginPage)
        self.controller.destroy()

    def clear(self, frame):
        pass

class SiteSummary(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.canvas = tk.Canvas(self, bg='red').pack(anchor='center', expand=True, fill='x')
        self.back_button = tk.Button(self.canvas, text='Back', command=self.handle_back_btn).pack(anchor='se')

        #self.canvas = tk.Canvas(self).pack()
        #self.label1 = tk.Label(self, text='Is this working?').pack()

    def populate_site_summary(self):
        please_wait_text = tk.StringVar()
        please_wait_text.set('Loading offline device summary, please wait...')
        please_wait = tk.Label(self.canvas, textvariable=please_wait_text).pack()
        increment = 100/len(self.controller.ui.controller.sites)
        progress = 0
        summary = {}

        for site in self.controller.ui.controller.sites:
            progress += increment
            offline_count = 0
            self.controller.ui.select_site(site.num)
            for device in site.devices:

                print(str(device.props['state']))
                if device.props['state'] == 0:
                    offline_count+=1
            print(offline_count)
            if offline_count > 0:
                summary.update({site:offline_count})
            print(str(progress)+'%')


        please_wait_text.set('')

        for site in summary.keys():

            tk.Label(tk.LabelFrame(self.canvas, text=site.name, bg='purple').pack(anchor='w'), text=site.name+' has '+str(summary[site])+ ' devices offline.').pack(anchor='nw')

    def handle_back_btn(self):
        self.controller.show_frame(MainPage)


if __name__=='__main__':
    app = PageContainer()
    app.mainloop()
