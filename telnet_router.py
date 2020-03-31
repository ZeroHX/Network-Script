"""
Telnet Router Module Version 1.2
Author: Pongpanit Aranratsopon, Jakkawan Intaratchaiyakij

This module help you easier telnet and config routers via python script.
There are many method of TN_ROUTER class those develop to use in PCN lab (IT-KMITL)
"""
import getpass
import telnetlib

#Pre-config
class TN_ROUTER:
    """
    TN_ROUTER class
    use instead of telnetlib.Telnet class encapsulate a lot of config commands to methods
    make communicate with telnet device much more comfortable + more reusability
    """

    #this attribute is the mark in begining of the line to check terminal mode
    mark = {"user":b'>', "priv":b'#', 'conf t':b'#'}

    def __init__(self, device, username, password, en_password):
        """initialize the TN_ROUTER object"""

        #Pre-Configuration
        self.device = device
        self.username = username
        self.password = password
        self.en_password = en_password
        self.status = "user"

        #Connect to device
        print("Connecting to ", self.device)
        self.tn = telnetlib.Telnet(self.device)
        print("Connected.")

        #Authentication method
        self.authen()

        #set terminal lenth to 0 method
        self.disable_pause()

        #get device hostname by get_device_name method
        self.hostname = self.get_device_name()
        print(self.hostname)

    def write_command(self, command = ''):
        """ Encode and Write the command """
        command = (command + '\n').encode()
        self.tn.write(command)

    def read_mark(self):
        """
        Use instead of read_until method. This method will read actually character automatically.
        and make router ready for new write command.
        """
        return self.tn.read_until(TN_ROUTER.mark[self.status])

    def strip_mark(self, message):
        """
        Strip string with hostname and mark when you use read_until at the end of txt
        use to formatting output string
        """
        return message.rstrip(self.hostname + TN_ROUTER.mark[self.status].decode())

    def check_change_mode(self, mode):
        """ Check that CLI is in specificed mode if not, change mode."""
        if self.status != mode:
            #This terminal is in lower mode than the new mode
            print('Wrong mode.now change to %s . . .'%mode)

            #User want to change mode to privillege mode
            if mode == 'priv':
                #In case of recent mode is configure terminal mode
                if self.status == 'conf t':
                    self.read_mark()
                    self.write_command('exit')
                    self.status = 'priv'
                #In case of recent mode is user mode
                else:
                    self.enable()
            #User want to change mode to configure terminal mode
            elif mode == 'conf t':
                self.config_terminal()

    def authen(self):
        """ Authentication to Device line """
        if self.username:
            self.tn.read_until(b'Username: ')
            self.write_command(self.username)
        if self.password:
            self.tn.read_until(b'Password: ')
            self.write_command(self.password)
        print("Authentation successful.")

    def disable_pause(self):
        """ Disable pause btw pages """
        self.read_mark()
        self.write_command("terminal length 0")
        print("Disable pause successful.")

    @staticmethod
    def save_as_txt(data, filename):
        """ Save data as txt file """
        with open(filename, 'w') as txt_file:
            txt_file.write(data + "\n")

    def enable(self):
        """ Enable privillege mode """
        self.read_mark()
        self.write_command('enable')
        self.tn.read_until(b'Password: ')
        self.write_command(self.en_password)
        self.status = 'priv'
        print('Now is privilege mode.')

    def config_terminal(self):
        """ Enter configure terminal mode """
        self.check_change_mode('priv')
        self.read_mark()
        self.write_command('conf t')
        self.status = 'conf t'
        print('Now is configure terminal mode.')

    def terminate(self):
        """ This is a """
        # if self.status == 'conf t':
        self.read_mark()
        self.write_command('end')
        self.read_mark()
        self.write_command('exit')
        self.tn.read_all()
        print("Finished.")

    def get_device_name(self):
        """return name of this device as string"""
        self.check_change_mode('priv')
        self.read_mark()
        print("show hostname by running config . . .")
        #show running config only line that has 'hostname' in it to get hostname
        self.write_command('show run | include hostname')
        #seperate hostname from output string
        name = self.read_mark().decode('utf-8').split('\n')[-1][:-1]
        print("hostname is", name)
        #prepare for another method to read_until again
        self.write_command('')
        return name

    def get_routing_table(self):
        """ return routing table of this device ass string """
        self.check_change_mode('priv')
        self.read_mark()
        print("show ip route . . .")
        #show routing table by 'show ip route' command
        self.write_command('show ip route')
        #seperate routing table from output string
        table = self.strip_mark(self.read_mark().decode('utf-8'))
        return table

    def get_router_spec(self):
        """ return router specification as string"""
        self.check_change_mode('priv')
        print("show version . . .")
        self.read_mark()
        self.write_command('show version')
        print("show version successful.")
        #seperate router specification from output string
        version = self.strip_mark(self.read_mark().decode('utf-8'))
        self.write_command('')
        return version

    def get_interface_summary(self):
        """ return router interface summary as string"""
        self.check_change_mode('priv')
        print("show interface summary . . .")
        self.read_mark()
        self.write_command('show interface summary')
        print("show interface summary successful.")
        #seperate router interface summary from output string
        summary = self.strip_mark(self.read_mark().decode('utf-8'))
        self.write_command('')
        return summary

    def get_router_interfaces(self):
        """
        return router interfaces as list of dict
        format :
        [
            {
            'Interface':'GigabitEthernet0/0/0',
            'IP-Address':'127.0.0.1',
            'OK?':'Yes',
            'Method':'unset',
            'Status':'up',
            'Protocol':'up'
            }, ...
        ]
        """
        self.check_change_mode('priv')
        print("show ip interface brief . . .")
        self.read_mark()
        self.write_command('show ip int br')
        interfaces = self.strip_mark(self.read_mark().decode('utf-8')).split('\n')
        # print(*interfaces, sep='\n')

        #formating output string into list of dicts
        col_name = interfaces[1].split()
        data = [row.split() for row in interfaces[2:-1:]]
        interfaces_list = [{col_name[col_no]:data[row_no][col_no] for col_no in range(len(col_name))}\
             for row_no in range(len(data))]

        self.write_command()

        return interfaces_list

    def get_connected_network(self):
        """
        return list of neighbour network as list of dict (used in eigrp auto config)
        format:
        [
            {
                'network_address':'10.0.0.0',
                'subnet_mask': 24
            }, ...
        ]
        """
        self.read_mark()
        self.check_change_mode('priv')
        self.write_command('show ip route | include C')

        #formating output string into list of dicts
        connected = self.strip_mark(self.read_mark().decode()).split('\n')
        connected = connected[2::]
        network_list = [{'network_address':line.split()[1].split('/')[0], \
            'subnet_mask':int(line.split()[1].split('/')[1])} for line in connected]

        self.write_command()
        return network_list

    def adjust_delay(self, target_int, delay, cancel = False):
        """
        set router target interface delay to specific value
        if cancle is True, delete delay config of target interface instead
        """
        print("Adjust delay. . .")
        self.check_change_mode("conf t")
        self.read_mark()
        self.write_command("int %s" % target_int)
        self.read_mark()
        if cancel:
            self.write_command("no delay")
            print("No delay for %s"%target_int)
        else:
            self.write_command("delay %d" % delay)
            print("Set router interface %s delay to %d."%(target_int, delay))

    def eigrp_config(self):
        """ Method for EIGRP routing protocol auto basic config"""
        #get connected network by get_connected_network method
        connected_list = self.get_connected_network()
        self.check_change_mode('conf t')
        self.read_mark()
        self.write_command('router eigrp 1') #set as to 1
        self.write_command('no auto-summary') #set no auto-summary
        for network in connected_list:
            self.read_mark()
            self.write_command("network %s 0.0.0.255"%network["network_address"])
        self.write_command("end")

    def show_version(self, filename):
        """ Show version of device and save as txt """
        version = self.get_router_spec()
        print("saving text file . . .")
        if not filename:
            filename = "Version_%s.txt"%self.device
        TN_ROUTER.save_as_txt(version, filename)
        print("saved.")

    def change_hostname(self, new_name):
        """ Change the hostname to new_hostname """
        self.check_change_mode('conf t')
        self.config_terminal()
        self.read_mark()
        self.write_command("hostname %s "%new_name)
        print("hostname was changed to %s"%new_name)
        self.hostname = new_name

    def change_password(self, new_pass):
        """ Change the password to new_pass """
        self.check_change_mode('conf t')
        self.read_mark()
        self.write_command("line vty 0 924")
        self.read_mark()
        self.write_command("password %s"%new_pass)
        self.read_mark()
        self.write_command("exit")
        print("password was changed to %s"%new_pass)

    def show_running(self, filename):
        """ Show running-config and save as txt file """
        print("show running . . .")
        self.check_change_mode('priv')
        self.read_mark()
        self.write_command('show run')
        print("show running-config successful.")
        running_config = self.read_mark().decode('utf-8')
        print("saving text file . . .")

        #Generate auto-filename if user not entering the filename
        if not filename:
            filename = "RunningConfig_%s.txt"%self.device
        TN_ROUTER.save_as_txt(running_config, filename)
        print("saved.")

    def show_running(self, filename):
        """ Show running config and save as txt file """
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



