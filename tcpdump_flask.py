import os
import subprocess
from collections import OrderedDict
import re

dump_pid = ''
tcpdump_running = False
save_filename = '001.pcap'

def set_pcap_filename(filename):
    global save_filename
    save_filename = filename

def tcpdump_is_running():
    global tcpdump_running
    return tcpdump_running

def tcpdump_run():
# sample tcpdump command string:
# tcpdump -XX -A -c  5 -w 0001.pcap -i eth0 src 192.168.0.2  dst 50.116.66.139 tcp/port 22
#   -c: capture specified number of packets
#   -A: displays the package in ASCII format
#   -XX: capture data of each packet including its link level header in HEX and ASCII
#   -w: capture and save the file in a .pcap format
#   -i: specify the interface to be captured on
#   tcp/port xx: capture specific port
#
# tcpdump -D
#   list number of available interfaces on the system
#
# tcpdump -r 0001.pcap
#   read and analyze captured packet
# 
# flag values:
    capture_value = 25
    global save_filename
    available_interfaces = []
    read_filename = '0001.pcap'
    capture_interface = 'eth1'
    source_ip = '192.168.0.10'
    destination_ip = '50.116.66.139'
    port = '22'
    tcp = 0
    udp = 0

    global tcpdump_running
    tcpdump_running = True



# flag booleans:
    flag_booleans = {'xx_flag': False, 'a_flag': False, 'c_flag': False, 'w_flag': True, 'i_flag': True,
                    'src_flag': False, 'dst_flag': False, 'port_flag': False, 'tcp_flag': False, 'udp_flag':False}

# Flag dictionary
    flags = OrderedDict([('-XX', 'data includes link level header in HEX and ASCII'),
            ('-A', 'displays the package in ASCII format'),
            ('-c', 'enter specified number of packets to capture'),
            ('-w', 'enter desired .pcap filename'),
            ('-D', 'list available interfaces on the system'),
            ('-r', 'enter .pcap filename to read'),
            ('-i', 'set capture interface'),
            ('src', 'enter source ip address to be captured'),
            ('dst', 'enter destination ip address to be captured'),
            ('port', 'enter port number to be captured'),
            ('tcp', 'capture only tcp traffic'),
            ('udp', 'capture only udp traffic'),]
        )
# Create list of keys so that we can access the keys via indexing
    keys = list(flags)

# String creation function
    def create_string():
        #start with an empty string
        tcpdump_str = 'tcpdump '
        if flag_booleans['xx_flag'] == True:
            tcpdump_str = tcpdump_str + keys[0]
        if flag_booleans['a_flag'] == True:
            tcpdump_str = tcpdump_str + keys[1]
        if flag_booleans['c_flag'] == True:
            tcpdump_str = tcpdump_str + keys[2] + ' ' + str(capture_value) + ' '
        if flag_booleans['w_flag'] == True:
            tcpdump_str = tcpdump_str + keys[3] + ' ' + save_filename + ' '
        if flag_booleans['i_flag'] == True:
            tcpdump_str = tcpdump_str + keys[6] + ' ' + capture_interface + ' '
        if flag_booleans['src_flag'] == True:
            tcpdump_str = tcpdump_str + keys[7] + ' ' + source_ip + ' '
        if flag_booleans['dst_flag'] == True:
            tcpdump_str = tcpdump_str + keys[8] + ' ' + destination_ip + ' '
        if flag_booleans['port_flag'] == True:
            tcpdump_str = tcpdump_str + keys[9] + ' ' + str(port) + ' '
        if flag_booleans['tcp_flag'] == True:
            tcpdump_str = tcpdump_str + keys[10]
        if flag_booleans['udp_flag'] == True:
            tcpdump_str = tcpdump_str + keys[11]
        return tcpdump_str.split()

    def set_flag_booleans():
        pass

    global dump_pid
    p = subprocess.Popen(create_string(), stdout=subprocess.PIPE)
    dump_pid = p.pid
    #dump_ppid = os.getppid()
    print('Process spawned with PPID and PID of: %s ' % p.pid)
    #subprocess.run(create_string(), shell=True)

def kill_process():
    global tcpdump_running
    global dump_pid
    os.system("kill %s" % (dump_pid))
    #subprocess.check_call(['sudo', 'kill', str(dump_pid)])
    tcpdump_running = False
    print('Process %s Killed.' % dump_pid)

def tcpdump_test():
    pattern = '[tcpdump] <defunct>'
    x = os.system("ps -fA | grep tcpdump")
    y = str(x)
    if re.search(pattern, y):
        print("tcpdump is not running")
    else:
        print("tcpdump is running")



