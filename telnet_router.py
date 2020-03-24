"""
Version 1.1
"""
import getpass
import telnetlib

#Pre-config
class TN_ROUTER:

    mark = {"user":b'>', "priv":b'#', 'conf t':b'(config)#'}
    def __init__(self, device, username, password, en_password):
        self.device = device
        self.username = username
        self.password = password
        self.en_password = en_password
        self.status = "user"

        #Connect to device
        print("Connecting to ", self.device)
        self.tn = telnetlib.Telnet(self.device)
        print("Connected.")
        self.disable_pause()

    def get_device_name(self):
        """return name of this device as string"""
        self.check_change_mode('priv')

        self.read_mark()
        print("show hostname by running config . . .")
        self.write_command('show run | include hostname')
        name = self.read_mark().decode('utf-8').replace('hostname ', '').split('\n')[0]
        print(f"hostname is {name}") 
        return name

    def get_routing_table(self):
        """ return routing table of this device ass string """
        self.check_change_mode('priv')        
        self.read_mark()
        print("show ip route . . .")
        self.write_command('show ip route')
        table = self.read_mark().decode('utf-8').rstrip(TN_ROUTER.mark[self.status])
        return table
    
    def get_router_spec(self):
        """ return router specification as string"""
        self.check_change_mode('priv')
        print("show version . . .")
        self.read_mark()
        self.write_command('show version')
        print("show version successful.")
        version = self.read_mark().decode('utf-8').rstrip(TN_ROUTER.mark[self.status])
        print(version)
        return version

    def get_router_interfaces(self):
        """ return router interfaces """
        self.check_change_mode('priv')
        print("show ip interface brief . . .")
        self.read_mark()
        self.write_command('show ip int br')
        interface = self.read_mark().decode('utf-8').rstrip(TN_ROUTER.mark[self.status])
        return interface

    def check_change_mode(self, mode):
        """check and change to specificed mode"""
        if self.status != mode:
            print('Wrong mode.now change to %s . . .'%mode)
            if mode == 'priv':
                self.enable()
            elif mode == 'conf t':
                self.config_terminal()

    def write_command(self, command):
        """ encode and write the command """
        command = (command + ' \n').encode()
        self.tn.write(command)

    def read_mark(self):
        self.tn.read_until(TN_ROUTER.mark[self.status]) 

    def authen(self):
        """ Authen to Device line """
        if self.username:
            self.tn.read_until(b'Username: ')
            self.write_command(self.username)
        if self.password:
            self.tn.read_until('Password: ')
            self.write_command(self.password)
            # tn.write(password.encode('ascii') + b'\n')

    def disable_pause(self):
        """ Disable pause btw pages """
        self.read_mark()
        self.write_command("terminal length 0")

    def show_version(self, filename):
        """ Show version of device and save as txt """
        version = self.get_router_spec()
        print("saving text file . . .")
        if not filename:
            filename = "Version_%s.txt"%self.device
        TN_ROUTER.save_as_txt(version, filename)
        print("saved.")

    @staticmethod
    def save_as_txt(data, filename):
        """ save data as txt file """
        with open(filename, 'w') as txt_file:
            txt_file.write(data + "\n")

    def enable(self):
        """ enable priv mode """
        self.read_mark()
        self.write_command('enable')
        self.tn.read_until(b'Password: ')
        self.write_command(self.en_password)
        self.status = 'priv'
        print('Now privilege mode.')

    def config_terminal(self):
        """ Enter config terminal mode """
        self.check_change_mode('priv')
        self.read_mark()
        self.write_command('conf t')
        self.status = 'conf t'
        print('Now is config terminal mode.')

    def change_hostname(self, new_name):
        self.check_change_mode('conf t')
            self.config_terminal()
        self.read_mark()
        self.write_command("hostname %s "%new_name)
        print("hostname was changed to %s"%new_name)

    def change_password()

    def show_running(self, filename):
        """show running config and save as txt file"""
        print("show running . . .")
        self.check_change_mode('priv')
        self.read_mark()
        self.write_command('show run')
        print("show running-config successful.")
        running_config = tn.read_until(TN_ROUTER.mark[self.status]).decode('utf-8')
        print("saving text file . . .")
        if not filename:
            filename = "RunningConfig_%s.txt"%self.device
        TN_ROUTER.save_as_txt(running_config, filename)
        print("saved.")

    def terminate(self):
        self.read_mark()
        self.write_command('end')
        self.tn.read_all()
        print("Finished.")
        return

