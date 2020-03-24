"""Change the name of Routers and their password too"""
import telnet_router
import json
def get_routers(filename):
    '''
    get routers info from ip in json_file
    [
        {
            "device":"127.0.0.1", 
            "username":"MarinePA", 
            "password":"cisco", 
            "en_password":"class"
        }, ...
    ]
    '''
    with open(filename, 'r') as json_file:
        add_list = json.loads(json_file.read())
    print("Addresses :" + str(add_list))
    routers = [telnet_router.TN_ROUTER(router['device'], router['username'], \
         router['password'], router['en_password']) for router in add_list]
    return routers


ip_count = 1
for ip in get_routers()['device']:
    router = telnet_router.TN_ROUTER(ip, '', 'cisco', 'class')
    router.authen()
    router.disable_pause()
    device_name = router.get_device_name()
    router.change_hostname(device_name)
    router.change_password('cisco%s'%ip_count)
    print(router.get_device_name())     #new hostname
    router.terminate()
    ip_count += 1
