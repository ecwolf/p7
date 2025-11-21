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
#topo.addrec_port_user(44)
# Second pipeline recirculation port for custom bandwidth
#topo.addrec_port_bw("16/-", 0)

topo.addports_file("portConfigs.txt")
#topo.addports_file("portConfigsDiferent.txt")

topo.tofinoVersion(1) #default is 1


#topo.definePipelines("p1", "spine", "p1", "spine")
topo.definePipelines("p1", "spine")

#topo.definePipelines("spine", "p1")

topo.addp4("p1", "p4src/simple_forward.p4")

topo.routing(2) #type for user defined routing, 0 for default routing


# addswitch(name, p4code)
topo.addswitch("sw1", "p1")

topo.addswitch("sw2", "p1")
topo.addswitch("sw3", "p1")
topo.addswitch("sw4", "p1")
topo.addswitch("sw5", "p1")

topo.addswitch("sw6", "p1")

topo.addswitch("sw7", "p1")
topo.addswitch("sw8", "p1")
topo.addswitch("sw9", "p1")
topo.addswitch("sw10", "p1")
topo.addswitch("sw11", "p1")

topo.addswitch("sw12", "p1")

topo.addswitch("sw13", "p1")



topo.addhost("h1","5/0", 164, 100000000000, "False", "False", 1920, "192.168.0.10")

topo.addhost("h2","6/0", 172, 100000000000, "False", "False", 1920, "192.168.0.20")

#topo.addhost("h2","1/0", 132, 10000000000, "False", "False", 1920, "192.168.0.20")

# addlink(node1, node2, bw, pkt_loss, latency, jitter, jitter percentage, packet loss model (optional))
# Default packet loss model is Gilbert-Elliott
# Optional a pure percentage validation drom can be selected by defining the pkt_loss_model=0
# e.g., topo.addlink("h1","sw1", 1000000000, 10, 10, 0, 100, pkt_loss_model=0)
topo.addlink("h1","sw1", 100000000000, 0, 0, 0, 100)
#topo.addlink("sw1","h2", 2000000000, 0, 0, 0, 100)

#topo.addlink("sw1","sw2", 100000000000, 0, 0, 0, 100)
#topo.addlink("sw3","sw2", 4000000000, 10, 10, 0, 100)
#topo.addlink("sw3","sw4", 4000000000, 10, 10, 0, 100)

topo.addlink("sw1","sw2", 100000000000, 0, 0, 0, 100)

topo.addlink("sw2","sw3", 100000000000, 0, 0, 0, 100)
topo.addlink("sw3","sw4", 100000000000, 0, 0, 0, 100)

topo.addlink("sw4","sw5", 100000000000, 0, 0, 0, 100)

topo.addlink("sw5","sw6", 100000000000, 0, 0, 0, 100)

topo.addlink("sw6","sw7", 100000000000, 0, 0, 0, 100)

topo.addlink("sw7","sw8", 100000000000, 0, 0, 0, 100)

topo.addlink("sw8","sw9", 100000000000, 0, 0, 0, 100)

topo.addlink("sw9","sw10", 100000000000, 0, 0, 0, 100)

topo.addlink("sw10","sw11", 100000000000, 0, 0, 0, 100)

topo.addlink("sw11","sw12", 100000000000, 0, 0, 0, 100)

topo.addlink("sw12","sw13", 100000000000, 0, 0, 0, 100)

topo.addlink("sw13","h2", 100000000000, 0, 0, 0, 100)


# add table entry sw1
topo.addtable('sw1','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','140')
topo.addactionvalue('sw', '1')
topo.insert()


# add table entry sw1
topo.addtable('sw1','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','132')
topo.addactionvalue('sw', '0')
topo.insert()


# add table entry sw2
topo.addtable('sw2','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','148')
topo.addactionvalue('sw', '2')
topo.insert()


# add table entry sw2
topo.addtable('sw2','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','140')
topo.addactionvalue('sw', '1')
topo.insert()


# add table entry sw3
topo.addtable('sw3','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','156')
topo.addactionvalue('sw', '3')
topo.insert()


# add table entry sw3
topo.addtable('sw3','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','148')
topo.addactionvalue('sw', '2')
topo.insert()



# add table entry sw4
topo.addtable('sw4','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','180')
topo.addactionvalue('sw', '4')
topo.insert()


# add table entry sw4
topo.addtable('sw4','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','156')
topo.addactionvalue('sw', '3')
topo.insert()


# add table entry sw5
topo.addtable('sw5','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','188')
topo.addactionvalue('sw', '5')
topo.insert()


# add table entry sw5
topo.addtable('sw5','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','180')
topo.addactionvalue('sw', '4')
topo.insert()


# add table entry sw6
topo.addtable('sw6','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','184')
topo.addactionvalue('sw', '6')
topo.insert()


# add table entry sw6
topo.addtable('sw6','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','188')
topo.addactionvalue('sw', '5')
topo.insert()


# add table entry sw7
topo.addtable('sw7','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','176')
topo.addactionvalue('sw', '7')
topo.insert()


# add table entry sw7
topo.addtable('sw7','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','184')
topo.addactionvalue('sw', '6')
topo.insert()


# add table entry sw8
topo.addtable('sw8','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','168')
topo.addactionvalue('sw', '8')
topo.insert()


# add table entry sw8
topo.addtable('sw8','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','176')
topo.addactionvalue('sw', '7')
topo.insert()



# add table entry sw9
topo.addtable('sw9','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','160')
topo.addactionvalue('sw', '9')
topo.insert()


# add table entry sw9
topo.addtable('sw9','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','168')
topo.addactionvalue('sw', '8')
topo.insert()


# add table entry sw10
topo.addtable('sw10','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','144')
topo.addactionvalue('sw', '10')
topo.insert()


# add table entry sw10
topo.addtable('sw10','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','160')
topo.addactionvalue('sw', '9')
topo.insert()


# add table entry sw11
topo.addtable('sw11','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','152')
topo.addactionvalue('sw', '11')
topo.insert()


# add table entry sw11
topo.addtable('sw11','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','144')
topo.addactionvalue('sw', '10')
topo.insert()


# add table entry sw12
topo.addtable('sw12','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','128')
topo.addactionvalue('sw', '12')
topo.insert()


# add table entry sw12
topo.addtable('sw12','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','152')
topo.addactionvalue('sw', '11')
topo.insert()


# add table entry sw13
topo.addtable('sw13','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','136')
topo.addactionvalue('sw', '13')
topo.insert()


# add table entry sw13
topo.addtable('sw13','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','128')
topo.addactionvalue('sw', '12')
topo.insert()


#Generate files
topo.verifier()
topo.generate_chassis()
topo.generate_ports()
topo.generate_p4rt()
topo.generate_bfrt()
topo.generate_p4code()
topo.generate_graph()
topo.parse_usercode()
topo.generate_setfiles()
topo.generate_multiprogram()
topo.printSwitches()
