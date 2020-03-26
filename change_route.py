"""
Change Route
    1   2   3   4   5   6
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
    """change route of source to destination to opposite route"""
    with open('PCs.json', 'r') as json_file:
        pc_hosts = json.loads(json_file.read())
    
    src_gw = pc_hosts[source]
    des_gw = pc_hosts[destination]
    src_gw_rt = int(src_gw.split(".")[2])
    des_gw_rt = int(des_gw.split(".")[2])
    with open('routers.json', 'r') as json_file:
        routers_info = json.loads(json_file.read())[src_gw_rt - 1]

    direction_map = "XCCUAA"[7-src_gw_rt:] + "XCCUAA"[:7-src_gw_rt]
    route_direction = direction_map[des_gw_rt - 1]
    if route_direction == 'C':
        third_oct = ''.join(sorted(["612345"[src_gw_rt], "612345"[(src_gw_rt+1)%6]]))
    elif route_direction == 'A':
        third_oct = ''.join(sorted(["612345"[src_gw_rt], "612345"[(src_gw_rt-1)%6]]))

    target_int_ip = ".".join(src_gw.split()[:2] + [str(third_oct)] + [str(src_gw_rt)])
    router = telnet_router.TN_ROUTER(routers_info["Device"], routers_info["username"], \
        routers_info["password"], routers_info["en_password"])
    target_int = find_int_from_ip(target_int_ip, router)
    if cancel:
        delay = 0
    else:
        delay = 100000
    router.adjust_delay(target_int, delay)

def find_int_from_ip(target, router):
    """find int from ip"""
    int_list = router.get_router_interfaces(routers_info)
    for interface in int_list:
        if interface['IP-Address'] == target:
            return interface['Interface']


change_route("A", "A'")
change_route("A", "A''")
change_route("A''", "A")
change_route("B", "B'")
change_route("B", "B''")
change_route("B''", "B")

    




