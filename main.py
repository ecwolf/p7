 ################################################################################
 # Copyright 2025 INTRIG
 #
 # Licensed under the Apache License, Version 2.0 (the "License");
 # you may not use this file except in compliance with the License.
 # You may obtain a copy of the License at
 #
 #     http://www.apache.org/licenses/LICENSE-2.0
 #
 # Unless required by applicable law or agreed to in writing, software
 # distributed under the License is distributed on an "AS IS" BASIS,
 # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 # See the License for the specific language governing permissions and
 # limitations under the License.
 ################################################################################

from src.data import *

topo = generator('main', sys.argv[1:])

# Stratum ip:port
# topo.addstratum("10.1.1.223:9559")

# Recirculation port default 68
topo.addrec_port(196)
topo.addrec_port_user(68)
# Second pipeline recirculation port for custom bandwidth
topo.addrec_port_bw("16/-", 0)

# addswitch(name)
topo.addswitch("sw1")
topo.addp4("p4src/p7calc.p4")

# addhost(name,port,D_P,speed_bps,AU,FEC,vlan)
# include the link configuration
topo.addhost("h1","1/0", 132, 10000000000, "False", "False", 1920, "192.168.0.10")
topo.addhost("h2","1/2", 134, 10000000000, "False", "False", 1920, "192.168.0.20")

# addlink(node1, node2, bw, pkt_loss, latency, jitter, jitter percentage, packet loss model (optional))
# Default packet loss model is Gilbert-Elliott
# Optional a pure percentage validation drom can be selected by defining the pkt_loss_model=0
# e.g., topo.addlink("h1","sw1", 1000000000, 10, 10, 0, 100, pkt_loss_model=0)
topo.addlink("h1","sw1", 1000000000, 10, 10, 0, 100)
topo.addlink("sw1","h2", 2000000000, 0, 0, 0, 100)

# add table entry sw1
topo.addtable('sw1','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('value','5')
topo.insert()

topo.addtable('sw1','SwitchIngress.calculate')
topo.addaction('SwitchIngress.operation_add')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('value','10')
topo.insert()

#Generate files
topo.generate_chassis()
topo.generate_ports()
topo.generate_p4rt()
topo.generate_bfrt()
topo.generate_p4code()
topo.generate_graph()
topo.parse_usercode()
topo.generate_setfiles()
topo.generate_multiprogram()