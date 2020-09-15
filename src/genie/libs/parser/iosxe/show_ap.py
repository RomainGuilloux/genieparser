import re

from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Any, Optional


# ===============================
# Schema for:
#  * 'show ap rf-profile summary'
# ===============================
class ShowApRfProfileSummarySchema(MetaParser):
    """Schema for show ap rf-profile summary."""

    schema = {
        "rf_profile_summary": {
            "rf_profile_count": int,
            "rf_profiles": {
                str: {
                    "rf_profile_name": str,
                    "band": str,
                    "description": str,
                    "state": str
                }
            }
        }
    }


# ===============================
# Parser for:
#  * 'show ap rf-profile summary'
# ===============================
class ShowApRfProfileSummary(ShowApRfProfileSummarySchema):
    """Parser for show ap rf-profile summary"""

    cli_command = 'show ap rf-profile summary'

    def cli(self, output=None):
        if output is None:
            out = self.device.execute(self.cli_command)
        else:
            out = output

        rf_profile_summary_dict = {}

        # Number of RF-profiles: 14
        #
        # RF Profile Name                  Band     Description                          State
        # ------------------------------------------------------------------------------------
        # Custom-RF_a                      5 GHz    Custom-RF_a_Desc                     Up
        # Custom-RF_b                      2.4 GHz  Custom-RF_b_Desc                     Up
        # Low_Client_Density_rf_5gh        5 GHz    pre configured Low Client Density rf Up
        # High_Client_Density_rf_5gh       5 GHz    pre configured High Client Density r Up
        # Low-Client-Density-802.11a       5 GHz                                         Up
        # Low_Client_Density_rf_24gh       2.4 GHz  pre configured Low Client Density rf Up
        # High-Client-Density-802.11a      5 GHz                                         Up
        # High_Client_Density_rf_24gh      2.4 GHz  pre configured High Client Density r Up
        # Low-Client-Density-802.11bg      2.4 GHz                                       Up
        # High-Client-Density-802.11bg     2.4 GHz                                       Up
        # Typical_Client_Density_rf_5gh    5 GHz    pre configured Typical Density rfpro Up
        # Typical-Client-Density-802.11a   5 GHz                                         Up
        # Typical_Client_Density_rf_24gh   2.4 GHz  pre configured Typical Client Densit Up
        # Typical-Client-Density-802.11bg  2.4 GHz                                       Up
        #


        # Number of RF-profiles: 14
        rf_profile_count_capture = re.compile(r"^Number\s+of\s+RF-profiles:\s+(?P<rf_profile_count>\d+)")
        # Custom-RF_a                      5 GHz    Custom-RF_a_Desc                     Up
        rf_profile_info_capture = re.compile(
            r"^(?P<rf_profile_name>\S+)\s+(?P<band>\S+\s+\S+)\s+(?P<description>.*)(?P<state>(Up|Down))")
        # RF Profile Name                  Band     Description                          State
        # ------------------------------------------------------------------------------------


        rf_profile_data = {}

        for line in out.splitlines():
            line = line.strip()
            # Number of RF-profiles: 14
            if rf_profile_count_capture.match(line):
                rf_profile_count_match = rf_profile_count_capture.match(line)
                groups = rf_profile_count_match.groupdict()
                rf_profile_count = int(groups['rf_profile_count'])
                if not rf_profile_summary_dict.get('rf_profile_summary', {}):
                    rf_profile_summary_dict['rf_profile_summary'] = {}
                rf_profile_summary_dict['rf_profile_summary']['rf_profile_count'] = rf_profile_count
                continue
            elif line.startswith('RF Profile Name'):
                continue
            elif line.startswith('-----'):
                continue
            # Custom-RF_a                      5 GHz    Custom-RF_a_Desc                     Up
            elif rf_profile_info_capture.match(line):
                rf_profile_info_match = rf_profile_info_capture.match(line)
                groups = rf_profile_info_match.groupdict()
                rf_profile_name = ''
                for k, v in groups.items():
                    if k == 'rf_profile_name':
                        rf_profile_name = v
                    v = v.strip()
                    if not rf_profile_summary_dict['rf_profile_summary'].get('rf_profiles', {}):
                           rf_profile_summary_dict['rf_profile_summary']['rf_profiles'] = {}
                    rf_profile_summary_dict['rf_profile_summary']['rf_profiles'][rf_profile_name] = {}
                    rf_profile_data.update({k: v})
                rf_profile_summary_dict['rf_profile_summary']['rf_profiles'][rf_profile_name].update(rf_profile_data)
                rf_profile_data = {}
                continue

        return rf_profile_summary_dict


# ====================================
# Schema for:
#  * 'show ap dot11 dual-band summary'
# ====================================
class ShowApDot11DualBandSummarySchema(MetaParser):
    """Schema for show ap dot11 dual-band summary."""

    schema = {
        "ap_dot11_dual-band_summary": {
            "index": {
                int: {
                    "ap_name": str,
                    "ap_mac_address": str,
                    "slot_id": int,
                    "admin_state": str,
                    "oper_state": str,
                    "width": int,
                    "tx_pwr": str,
                    "mode": str,
                    "subband": str,
                    "channel": str
                }
            }
        }
    }


# ====================================
# Parser for:
#  * 'show ap dot11 dual-band summary'
# ====================================
class ShowApDot11DualBandSummary(ShowApDot11DualBandSummarySchema):
    """Parser for show ap dot11 dual-band summary"""

    cli_command = 'show ap dot11 dual-band summary'

    def cli(self, output=None):
        if not output:
            output = self.device.execute(self.cli_command)

        ret_dict = {}

        # aa-test-4800                 64d8.14ec.1120  0     Enabled       Down           20     *1/8 (23 dBm)   Local   All        (6)*
        ap_info_capture = re.compile(
            r"^(?P<ap_name>\S+)\s+(?P<ap_mac_address>\S+)\s+(?P<slot_id>\d+)\s+(?P<admin_state>(Enabled|Disabled))\s+(?P<oper_state>\S+)\s+(?P<width>\d+)\s+(?P<tx_pwr>(N\/A|\*.*m\)))\s+(?P<mode>\S+)\s+(?P<subband>\S+)\s+(?P<channel>\S+)$")

        ap_index = 0

        for line in output.splitlines():
            line = line.strip()

            # aa-test-4800                 64d8.14ec.1120  0     Enabled       Down           20     *1/8 (23 dBm)   Local   All        (6)*
            m = ap_info_capture.match(line)
            if m:
                groups = m.groupdict()
                ap_index += 1

                if not ret_dict.get('ap_dot11_dual-band_summary'):
                    ret_dict['ap_dot11_dual-band_summary'] = {"index": {}}
                ret_dict['ap_dot11_dual-band_summary']["index"][ap_index]  = {
                    'ap_name': groups['ap_name'],
                    'ap_mac_address': groups['ap_mac_address'],
                    'slot_id': int(groups['slot_id']),
                    'admin_state': groups['admin_state'],
                    'oper_state': groups['oper_state'],
                    'width': int(groups['width']),
                    'tx_pwr': groups['tx_pwr'],
                    'mode': groups['mode'],
                    'subband': groups['subband'],
                    'channel': groups['channel']
                }

        return ret_dict