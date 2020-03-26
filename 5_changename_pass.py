"""Change the name of Routers and their password too [5]"""
import telnet_router
import json
def get_routers(filename):
    """
    connect to routers from ip in json_file and return list of TN_ROUTER obj
    format:
    [
        {
            "device":"127.0.0.1", 
            "username":"MarinePA", 
            "password":"cisco", 
            "en_password":"class"
        }, ...
    ]
    then create TN_ROUTER objects connect to all routers and return them.
    """
    with open(filename, 'r') as json_file:
        add_list = json.loads(json_file.read())
    print("Addresses :" + str(add_list))
    routers = [telnet_router.TN_ROUTER(router['device'], router['username'], \
         router['password'], router['en_password']) for router in add_list]
    return routers

#Count the Router number
ip_count = 1
for router in get_routers('routers.json'):
    #Get router name from method getter of TN_ROUTER
    device_name = router.get_device_name()
    print("Starting config %s"%device_name)

    #Change to new hostname from method of TN_ROUTER
    router.change_hostname(device_name+'s') 
    print("New hostname :",router.get_device_name())   #Show new hostname
    new_pass = 'cisco%d'%ip_count

    #Change to new password  from method of TN_ROUTER
    router.change_password(new_pass)
    print(new_pass)    #Show new password (FOR TESTING!)
    print("Change password.")
    ip_count += 1      
