"""
Change Route change route to opposite way in ring topology [6 & 7]
Normal Route Table
S/D 1   2   3   4   5   6
1   X   C   C   U   A   A   
2   A   X   C   C   U   A
3   A   A   X   C   C   U
4   U   A   A   X   C   C   
5   C   U   A   A   X   C
6   C   C   U   A   A   X
X is for not remote
C for clockwise
A for anti-clockwise
U for unknown
"""
import json
import telnet_router

def change_route(source, destination, cancel=False):
    """
    change route of source to destination to opposite route
    - Get PCs hostname and thier gateway to use in target interface calculation
    - Calculate ip of target interface to change delay config
    - Find target interface via ip and get_router_interfaces method of TN_ROUTER object
    - Program to delay config at target interface
    """
    print(source, destination)

    #read PCs.json that contains PCs hostname and thier gateway
    with open('PCs.json', 'r') as json_file:
        pc_hosts = json.loads(json_file.read())
    
    #get gateway of source and destination
    src_gw = pc_hosts[source]
    des_gw = pc_hosts[destination]

    #get router number from gateway ip (router interfaces ip and topology router number are consistency)
    src_gw_rt = int(src_gw.split(".")[2])
    des_gw_rt = int(des_gw.split(".")[2])

    #get specificed router by router number
    with open('routers.json', 'r') as js_file:
        routers_info = json.loads(js_file.read())[src_gw_rt - 1]
    # print(routers_info)

    #get table row output use a little pattern solution to archive it.
    direction_map = "XCCUAA"[7-src_gw_rt:] + "XCCUAA"[:7-src_gw_rt]
    #get table output by calling index
    route_direction = direction_map[des_gw_rt - 1]
    print("direction", route_direction)

    #get actual target interface third octed ip (work different in clockwise and counter clockwise)
    if route_direction == 'C':
        third_oct = ''.join(sorted(["612345"[src_gw_rt%6], "612345"[(src_gw_rt+1)%6]]))
    elif route_direction == 'A':
        third_oct = ''.join(sorted(["612345"[src_gw_rt%6], "612345"[(src_gw_rt-1)%6]]))
    else:
        return #if X (not a remote) or U (unknown) there is no need to do delay config
    print("third_oct", third_oct)
    # print()

    #formatting target interface ip
    target_int_ip = ".".join(src_gw.split(".")[:2] + [str(third_oct)] + [str(src_gw_rt)])

    #create TN_ROUTER object and connect to target interface's router
    router = telnet_router.TN_ROUTER(routers_info["device"], routers_info["username"], \
        routers_info["password"], routers_info["en_password"])
    #find target interface via find_int_from_ip using target interface ip
    target_int = find_int_from_ip(target_int_ip, router)
    print(target_int_ip)
    print(target_int)
    #set delay of that interface to 1M
    router.adjust_delay(target_int, 1000000, cancel)
    router.terminate() #terminate connection

def find_int_from_ip(target, router):
    """find int from ip"""
    int_list = router.get_router_interfaces()
    print(int_list)
    for interface in int_list:
        if interface['IP-Address'] == target:
            return interface['Interface']


def opposite_way(cancel = False):
    """ Change paths to opposite route """
    change_route("A", "A'", cancel)
    change_route("A'", "A''",  cancel)
    change_route("A''", "A",  cancel)
    change_route("B", "B'",  cancel)
    change_route("B'", "B''",  cancel)
    change_route("B''", "B",  cancel)

opposite_way() #use to delay config at interfaces and change prefered route
# opposite_way(True) #use to delete delay config [7]
    




