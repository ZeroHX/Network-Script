import getpass
import telnetlib

#Pre-config
class TN_ROUTER:
    
    mark = {"user":b'>', "priv":b'#'}
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

    def authen(self):
        """Authen to Device line"""
        if self.username:
            self.tn.read_until(b'Username: ' + b'\n')
            self.tn.write(self.username.encode())
        if self.password:
            self.tn.read_until(b'Password: ')
            self.tn.write(self.password.encode() + b'\n')
            # tn.write(password.encode('ascii') + b'\n')

    def disable_pause(self):
        """Disable pause btw pages"""
        self.tn.read_until(TN_ROUTER.mark[self.status])
        self.tn.write(b"terminal length 0\n")

    def show_version(self, filename):
        """Show version of device and save as txt"""
        print("show version . . .")
        self.tn.read_until(TN_ROUTER.mark[self.status])
        self.tn.write(b'show version')
        print("show version successful.")
        version = self.tn.read_until(TN_ROUTER.mark[self.status]).decode('utf-8')
        print("saving text file . . .")
        TN_ROUTER.save_as_txt(version, filename)
        print("saved.")

    @staticmethod
    def save_as_txt(data, filename):
        """save data as txt file"""
        with open(filename, 'w') as txt_file:
            txt_file.write(data + "\n")

    def enable(self):
        """enable priv mode"""
        self.tn.read_until(TN_ROUTER.mark[self.status])
        self.tn.write(b'enable \n')
        self.tn.read_until(b'Password: ')
        self.tn.write(self.en_password.encode() + b'\n')
        self.status = 'priv'
        print('enabled.')

    def show_running(self, filename):
        """show running config and save as txt file"""
        print("show running . . .")
        if self.status != 'priv':
            print('Wrong mode.')
            return
        self.tn.read_until(TN_ROUTER.mark[self.status])
        self.tn.write(b'show run')
        print("show running-config successful.")
        running_config = tn.read_until(TN_ROUTER.mark[self.status]).decode('utf-8')
        print("saving text file . . .")
        TN_ROUTER.save_as_txt(running_config, filename)
        print("saved.")

    def terminate(self):
        self.tn.read_until(TN_ROUTER.mark[self.status])
        self.tn.write(b'exit \n')
        self.tn.read_all() 




