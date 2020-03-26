import telnet_router
"""Testing"""
router_1 = telnet_router.TN_ROUTER('10.30.7.1', '', 'cisco', 'class')
router_1.authen()
router_1.show_running('')
router_1.terminate()