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
        print("show version . . .")
        self.read_mark()
        self.write_command('show version')
        print("show version successful.")
        version = self.read_mark().decode('utf-8')
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
        if self.status != 'priv':
            print("Wrong mode.now change to priv . . .")
            self.enable()
        self.read_mark()
        self.write_command('conf t')
        self.status = 'conf t'
        print('Now is config terminal mode.')

    def change_hostname(self, new_name):
        if self.status != 'conf t':
            print("Wrong mode. now change to configure terminal mode. . .")
            self.config_terminal()
        self.read_mark()
        self.write_command("hostname %s "%new_name)
        print("hostname was changed to %s"%new_name)



    def show_running(self, filename):
        """show running config and save as txt file"""
        print("show running . . .")
        if self.status != 'priv':
            print('Wrong mode. now change to privilege mode . . .')
            self.enable()
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

