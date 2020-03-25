import telnet_router

router_1 = telnet_router.TN_ROUTER('10.30.7.1', '', 'cisco', 'class')
router_1.show_version('router1_version.txt')
router_1.terminate()
