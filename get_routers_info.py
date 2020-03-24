"""Get Router Info"""
import telnet_router
import json
def get_routers(filename):
    '''
    connect to routers from ip in json_file and return list of TN_ROUTER obj
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

def get_routers_info():
    """get all router info and save into file"""
    routers = get_routers('xxx.json')
    routers_info_list = [\
        {'name':router.get_device_name(), 'spec':router.get_router_spec(), \
            'interface':router.get_router_interfaces(), 'routing table':router.get_routing_table()} \
        for router in routers]
    data = ""
    for router_info in routers_info_list:
        data += router_info['name'] + '\n====Specification====\n'
        data += router_info['spec'] + '\n====Interfaces====\n'
        data += '\n'.join([''.join([str(k) + ": " + interfaces[k]]) + '\n' \
            for interface in router_info['interface']]) + '\n====Routing Table====\n'
        data += router_info['routing table'] + '\n'
    
    with open('routers_info.txt', 'w') as text_file:
        text_file.write(data)
    

get_routers_info()
