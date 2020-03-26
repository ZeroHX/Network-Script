"""This script use to auto EIGRP basic configuration"""
import telnet_router

# router_1 = telnet_router.TN_ROUTER('10.30.7.1', '', 'cisco', 'class')
# router_1 = telnet_router.TN_ROUTER('100.1.12.2', '', 'cisco', 'class')
router_1 = telnet_router.TN_ROUTER('100.1.16.6', '', 'cisco', 'class')

router_1.eigrp_config()
router_1.terminate()
