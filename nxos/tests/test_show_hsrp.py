
# Python
import re
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Parser
from parser.nxos.show_hsrp import ShowHsrpSummary, ShowHsrpAll

# Metaparser
from metaparser.util.exceptions import SchemaEmptyParserError


# ======================================
#   Unit test for 'show hsrp summary'       
# ======================================

class test_show_hsrp_summary(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
    'hsrp_summary': {
        'active': 0,
        'global_hsrp_bfd': 'enabled',
        'intf_total': 1,
        'listen': 0,
        'nsf': 'enabled',
        'nsf_time': 10,
        'pkt_unknown_groups': 0,
        'rx_good': 0,
        'standby': 0,
        'total_groups': 3,
        'total_mts_rx': 85,
        'tx_fail': 0,
        'tx_pass': 0,
        'v1_ipv4': 0,
        'v2_ipv4': 3,
        'v2_ipv6': 0,
        'v6_active': 0,
        'v6_listen': 0,
        'v6_standby': 0}}

    golden_output = {'execute.return_value': '''
        HSRP Summary:

        Extended-hold (NSF) enabled, 10 seconds 
        Global HSRP-BFD enabled

        Total Groups: 3
             Version::    V1-IPV4: 0       V2-IPV4: 3      V2-IPV6: 0   
               State::     Active: 0       Standby: 0       Listen: 0   
               State::  V6-Active: 0    V6-Standby: 0    V6-Listen: 0   

        Total HSRP Enabled interfaces: 1

        Total Packets: 
                     Tx - Pass: 0       Fail: 0
                     Rx - Good: 0      

        Packet for unknown groups: 0

        Total MTS: Rx: 85
        '''}

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        hsrp_summary_obj = ShowHsrpSummary(device=self.device)
        parsed_output = hsrp_summary_obj.parse()
        #import pprint ; pprint.pprint(parsed_output)
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        hsrp_summary_obj = ShowHsrpSummary(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = hsrp_summary_obj.parse()


# ======================================
#   Unit test for 'show hsrp all'       
# ======================================

class test_show_hsrp_all(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output = {
    'hsrp_all': {
        'group': {
            0: {
                'interface': {
                    'Ethernet4/1': {
                        'address_family': {
                            'ipv4': {
                                'active_router': 'unknown',
                                'authentication_text': 'cisco123',
                                'configured_priority': 110,
                                'hellotime': 1,
                                'holdtime': 3,
                                'ip_redundancy_name': 'hsrp-Eth4/1-0',
                                'last_state_change': 'never',
                                'local_state': 'initial(interface '
                                               'down)',
                                'lower_fwd_threshold': 1,
                                'num_state_changes': 0,
                                'preempt': True,
                                'priority': 110,
                                'standby_router': 'unknown',
                                'upper_fwd_threshold': 110,
                                'version': 2,
                                'virtual_ip_address': '192.168.1.254',
                                'virtual_mac_addr': '0000.0c9f.f000',}}}}}}}}

    golden_output = {'execute.return_value': '''
    Ethernet4/1 - Group 0 (HSRP-V2) (IPv4)
      Local state is Initial(Interface Down), priority 110 (Cfged 110), may preempt
        Forwarding threshold(for vPC), lower: 1 upper: 110 
      Hellotime 1 sec, holdtime 3 sec
      Virtual IP address is 192.168.1.254 (Cfged)
      Active router is unknown
      Standby router is unknown 
      Authentication MD5, key-string "cisco123"
      Virtual mac address is 0000.0c9f.f000 (Default MAC)
      0 state changes, last state change never
      IP redundancy name is hsrp-Eth4/1-0 (default)
      '''}



    golden_parsed_output_1 = {
        "hsrp_all": {
              "group": {
                   0: {
                        "interface": {
                             "Ethernet1/3": {
                                  "address_family": {
                                       "ipv4": {
                                            "standby_expire": 2.429,
                                            "virtual_mac_addr": "0000.0c9f.f000",
                                            "standby_router": "192.168.1.2",
                                            "priority": 110,
                                            "virtual_ip_address": "192.168.1.254",
                                            "ip_redundancy_name": "hsrp-Eth1/3-0",
                                            "preempt": True,
                                            "active_priority": 110,
                                            "last_state_change": "00:01:43",
                                            "configured_priority": 110,
                                            "holdtime": 3,
                                            "authentication_text": "cisco123",
                                            "num_state_changes": 10,
                                            "version": 2,
                                            "hellotime": 1,
                                            "active_router": "local",
                                            "standby_priority": 90,
                                            "local_state": "active",
                                            "upper_fwd_threshold": 110,
                                            "lower_fwd_threshold": 0
                                       }
                                  }
                             }
                        }
                   },
                   2: {
                        "interface": {
                             "Ethernet1/3": {
                                  "address_family": {
                                       "ipv6": {
                                            "standby_expire": 8.96,
                                            "virtual_mac_addr": "0005.73a0.0002",
                                            "standby_router": "fe80::20c:29ff:fe69:14bb",
                                            "priority": 100,
                                            "authentication_text": "cisco",
                                            "ip_redundancy_name": "hsrp-Eth1/3-2-V6",
                                            "active_priority": 100,
                                            "last_state_change": "02:43:40",
                                            "configured_priority": 100,
                                            "holdtime": 10,
                                            "local_state": "active",
                                            "num_state_changes": 2,
                                            "lower_fwd_threshold": 0,
                                            "hellotime": 3,
                                            "active_router": "local",
                                            "standby_priority": 90,
                                            "upper_fwd_threshold": 100,
                                            "secondary_vips": "192:168::1",
                                            "virtual_ip_address": "fe80::5:73ff:fea0:2",
                                            "version": 2
                                       },
                                       "ipv4": {
                                            "virtual_mac_addr": "0000.0c9f.f002",
                                            "standby_router": "unknown",
                                            "priority": 1,
                                            "authentication_text": "cisco",
                                            "ip_redundancy_name": "hsrp-Eth1/3-2",
                                            "configured_priority": 1,
                                            "last_state_change": "never",
                                            "holdtime": 10,
                                            "local_state": "disabled(virtual ip not cfged)",
                                            "num_state_changes": 0,
                                            "lower_fwd_threshold": 0,
                                            "hellotime": 3,
                                            "active_router": "unknown",
                                            "upper_fwd_threshold": 1,
                                            "version": 2
                                       }
                                  }
                             }
                        }
                   }
              }
         }
    }

    golden_output_1 = {'execute.return_value': '''
      Ethernet1/3 - Group 0 (HSRP-V2) (IPv4)
        Local state is Active, priority 110 (Cfged 110), may preempt
          Forwarding threshold(for vPC), lower: 0 upper: 110 
        Hellotime 1 sec, holdtime 3 sec
        Next hello sent in 0.502000 sec(s)
        Virtual IP address is 192.168.1.254 (Cfged)
        Active router is local
        Standby router is 192.168.1.2 , priority 90 expires in 2.429000 sec(s)
        Authentication MD5, key-string "cisco123"
        Virtual mac address is 0000.0c9f.f000 (Default MAC)
        10 state changes, last state change 00:01:43
        IP redundancy name is hsrp-Eth1/3-0 (default)

      Ethernet1/3 - Group 2 (HSRP-V2) (IPv4)
        Local state is Disabled(Virtual IP not cfged), priority 1 (Cfged 1)
          Forwarding threshold(for vPC), lower: 0 upper: 1 
        Hellotime 3 sec, holdtime 10 sec
        Virtual IP address is unknown 
        Active router is unknown
        Standby router is unknown 
        Authentication text "cisco"
        Virtual mac address is 0000.0c9f.f002 (Default MAC)
        0 state changes, last state change never
        IP redundancy name is hsrp-Eth1/3-2 (default)

      Ethernet1/3 - Group 2 (HSRP-V2) (IPv6)
        Local state is Active, priority 100 (Cfged 100)
          Forwarding threshold(for vPC), lower: 0 upper: 100 
        Hellotime 3 sec, holdtime 10 sec
        Next hello sent in 0.455000 sec(s)
        Virtual IP address is fe80::5:73ff:fea0:2 (Auto)
        Active router is local
        Standby router is fe80::20c:29ff:fe69:14bb , priority 90 expires in 8.960000 sec(s)
        Authentication text "cisco"
        Virtual mac address is 0005.73a0.0002 (Default MAC)
        2 state changes, last state change 02:43:40
        IP redundancy name is hsrp-Eth1/3-2-V6 (default)
        Secondary VIP(s):
                        192:168::1
      '''}

    def test_golden(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output)
        hsrp_all_obj = ShowHsrpAll(device=self.device)
        parsed_output = hsrp_all_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output)

    def test_golden_1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_1)
        hsrp_all_obj = ShowHsrpAll(device=self.device)
        parsed_output = hsrp_all_obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_1)

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        hsrp_all_obj = ShowHsrpAll(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = hsrp_all_obj.parse()


if __name__ == '__main__':
    unittest.main()

# vim: ft=python et sw=4
