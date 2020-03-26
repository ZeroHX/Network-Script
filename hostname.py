import telnet_router
"""Testing"""
router_1 = telnet_router.TN_ROUTER('10.30.7.1', '', 'cisco', 'class')
router_1.authen()
router_1.disable_pause()
router_1.change_hostname("R1s")
router_1.terminate()