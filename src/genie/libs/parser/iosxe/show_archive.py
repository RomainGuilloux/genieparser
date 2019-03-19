''' show_archive.py

IOSXE parsers for the following show commands:
    * show archive
    * show archive config differences
    * show archive config differences <fileA> <fileB>
    * show archive config differences <fileA>
    * show archive config incremental-diffs <fileA>
'''

# Python
import re

# Metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Optional


# =============================================
# Parser for 'show archive'
# =============================================

class ShowArchiveSchema(MetaParser):
    """
    Schema for show archive
    """

    schema = {'archive': {
                'total': int,
                Optional('max_archive_configurations'): int,
                'most_recent_file': str,
                Any(): {
                    'file': str,
                },
            }
        }

class ShowArchive(ShowArchiveSchema):
    """ Parser for show archive """

    # Parser for 'show archive'
    cli_command = 'show archive'

    def cli(self,output=None):
        if output is None:
            # excute command to get output
            out = self.device.execute(self.cli_command)
        else:
            out = output

        # initial variables
        ret_dict = {}

        for line in out.splitlines():
            line = line.strip()

            # The maximum archive configurations allowed is 10.
            p1 = re.compile(r'^The +maximum +archive +configurations +allowed +is +(?P<max>\d+)\.$')
            m = p1.match(line)
            if m:
                if 'archive' not in ret_dict:
                    ret_dict['archive'] = {}
                ret_dict['archive']['max_archive_configurations'] = int(m.groupdict()['max'])
                continue

            # There are currently 1 archive configurations saved.
            p2 = re.compile(r'^There +are +currently +(?P<total>\d+) +archive +configurations +saved\.$')
            m = p2.match(line)
            if m:
                if 'archive' not in ret_dict:
                    ret_dict['archive'] = {}
                    
                ret_dict['archive']['total'] = int(m.groupdict()['total'])
                continue

            # 1        bootflash:uncfgIntfgigabitethernet0_0_0-Sep-27-15-04-18.414-PDT-0 <- Most Recent
            p3 = re.compile(r'^(?P<num>[0-9]+) +'
                             '(?P<file>[\w\:\-\.]+)(?P<recent> +\<\- +Most +Recent)?$')
            m = p3.match(line)
            if m:
                num = m.groupdict()['num']
                file = m.groupdict()['file']
                recent = m.groupdict()['recent']

                if 'archive' not in ret_dict:
                    ret_dict['archive'] = {}

                if num not in ret_dict['archive']:
                    ret_dict['archive'][num] = {}

                ret_dict['archive'][num]['file'] = file
                if recent:
                    ret_dict['archive']['most_recent_file'] = file                
                continue

        return ret_dict

# ====================================================
# Parser for 'show archive config differences'
# ====================================================
class ShowArchiveConfigDifferencesSchema(MetaParser):
    """
    Schema for the following commands
    * show archive config differences
    * show archive config differences {fileA} {fileB}
    * show archive config differences {fileA}
    * show archive config incremental-diff {fileA}
    """
    
    schema = {
            'diff': {
                'index': { Any():{
                    Optional('before'): list,
                    'after': list
                    }
                }
            }
        }

class ShowArchiveConfigDifferences(ShowArchiveConfigDifferencesSchema):
    """ Parser for the following commands:
        * show archive config differences
        * show archive config differences {fileA} {fileB}
        * show archive config differences {fileA}
    """

    cli_command = ['show archive config differences', 
                'show archive config differences {fileA} {fileB}',
                'show archive config differences {fileA}'
            ]

    def cli(self, fileA='', fileB='', cmd='', output=None):
        if output is None:
            # execute command to get output
            if fileA and fileB:
                command = self.cli_command[1].format(fileA=fileA, fileB=fileB)
            elif fileA:
                if cmd:
                    command = cmd.format(fileA=fileA)
                else:
                    command = self.cli_command[2].format(fileA=fileA)
            else:
                command = self.cli_command[0]
            out = self.device.execute(command)
        else:
            out = output

        # initial varaiables
        ret_dict = {}
        contextual_found = False
        index = 0
        is_new_index = ''
        
        # !Contextual Config Diffs:
        p1 = re.compile(r'^\s*!Contextual +Config +Diffs:$')
        # +hostname Router1
        p2 = re.compile(r'^\s*\+(?P<line_info>[\w\W]+)$')
        # -hostname Router2
        p3 = re.compile(r'^\s*\-(?P<line_info>[\w\W]+)$')
        # !List of commands:
        p4 = re.compile(r'^\s*!List +of +commands:$')
        # hostname Router3
        p5 = re.compile(r'^\s*(?P<line_info>([\w\W]+))$')

        for line in out.splitlines():
            line = line.strip()
            if not cmd:
                if not contextual_found:
                    #!Contextual Config Diffs
                    m = p1.match(line)
                    if m:
                        contextual_found = True
                        contextual_config_diffs = ret_dict.setdefault('diff',{}).\
                                                setdefault('index',{})
                        continue
                else:
                    # +hostname Router1
                    m = p2.match(line)
                    if m:
                        group = m.groupdict()
                        if is_new_index == '':
                            index+=1
                            index_dict = contextual_config_diffs.setdefault\
                                        (index, {'before': [],'after': []})
                        index_dict['after'].append(group['line_info'])
                        is_new_index = '+'
                        continue
                    # -hostname Router2
                    m = p3.match(line)
                    if m:
                        group = m.groupdict()
                        if is_new_index != '-':
                            index+=1
                            index_dict = contextual_config_diffs.setdefault\
                                        (index, {"before": [],"after": []})
                        index_dict['before'].append(group['line_info'])
                        is_new_index = '-'
                        continue
            else:
                # !List of commands:
                m = p4.match(line)
                if m:
                    incremental_diffs = ret_dict.setdefault('diff',{}).\
                                                setdefault('index',{}).\
                                                setdefault(1, {}).\
                                                setdefault('after',[])
                    continue
                # hostname router 192.168.5.2/22
                # end
                m = p5.match(line)
                if m:
                    group = m.groupdict()
                    incremental_diffs.append(group['line_info'])
                    continue
        return ret_dict

class ShowArchiveConfigIncrementalDiffs(ShowArchiveConfigDifferences):
    """ Parser for show archive config incremental-diffs <fileA>"""
    
    cli_command = 'show archive config incremental-diffs {fileA}'
    
    def cli(self,fileA='', output=None):
        return super().cli(fileA=fileA,cmd=self.cli_command,output=output)

