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
for router in get_routers('routers.json'):
    # router = telnet_router.TN_ROUTER(r['device'], '', 'cisco', 'class')
    # router.authen()
    # router.disable_pause()

    device_name = router.get_device_name()
    print("starting config??? %s"%device_name)
    router.change_hostname(device_name+'s')
    print("New hostname :",router.get_device_name())     #new hostname
    new_pass = 'cisco%d'%ip_count
    router.change_password(new_pass)
    print(new_pass)
    print("Change password.")     #new hostname
    # router.terminate()
    ip_count += 1
