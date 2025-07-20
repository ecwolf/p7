P7 (P4 Programmable Patch Panel): an instant 100G emulated network testbed in a pizza box
==

## Updates of this branch: routing exposed to the user and using loopback ports to increase P7 scalability.
Now each link created using P7 will map this link to a pair of loopback ports to process this link. It increases the P7 scalability to up to 14 links of 100Gbps (considering Tofino 1 of 32 ports and two physical hosts connected).

### Important assumptions/limitations:
- For now we just support Tofino 1, and switches with 2 pipes.
- P7 will always run on the pipe 1, and the user P4 code on pipe 0. It means that the physical hosts should be connected in pipe 1 ports. Pipe 1 ports are the ports with ID (D_P) from 128 to 191. Pipe 0 are ports with D_P between 0-63.
- Latency/ jitter are not working properly with this new update, so avoid use it before the next update.
- The loopback ports scalability improvement just work with the user-defined routing.
- Maybe the user-defined routing included bugs in the other routings (dijkstra and polka). So if you are going to use these routings, do not use this version.
- P7 solves the user tables atomatically (by adding a new key in all tables on your p4 code), but still not solve the registers. It means that if you are using registers, you need to manage you to split your registers beetween your emulated switches.
- Currently P7 just support user p4 codes totally based on ingress prossesing, If your code has something in the egress pipeline, it now will be executed.

### Changes and How to Use:
First, we introduced a new command to define the host as user-defined. So you need to include this in your main.py
```
# The parameter "2" define the routing as user defined. The other options are "1" for default routing, and "2" for polka routing.
topo.routing(2)
```

Now you also need to create a file containing your ports information. We need this because each Tofino model has different relations between ports/D_P. So in order to configure the ports in loopback, we need these information.

So, you may create a file with the output of the command `show -a` in your port manager. Take a look in our "portConfigs.txt" file, the output should be similar.
So, you need to pass this file for P7 through the command:
```
topo.addports_file("portConfigs.txt")
```
Note that if you not pass this file, P7 cannot configure the ports, and if you pass wrong information it will result in erros in the configuration.

After that you can define your topology as usual in the `main.py` script. For now you do not need to define the table entries, because this will be defined after the next step.


With the topology defined, you need to run the command below to generate and compile all the files:
```
python3 main.py -c
```

If is everything OK, after the codes compile you will receive an output like that: 
```
#example with two switches and three hosts in the topology.
Switches defined:
        Switch sw1 (ID (rec.sw_id): 0)
                To forward to link h1 <--> sw1  use rec.sw = 0  and ucast_egress_port = 132
                To forward to link sw1 <--> sw2  use rec.sw = 1  and ucast_egress_port = 134
        Switch sw2 (ID (rec.sw_id): 1)
                To forward to link sw1 <--> sw2  use rec.sw = 1  and ucast_egress_port = 134
                To forward to link sw2 <--> h2  use rec.sw = 2  and ucast_egress_port = 140
```
This information can be used to create your table entries and define your routing.
Some information about this example:
 - In your p4 code, when you receive a packet  with hdr.rec.sw_id == 0 you know that the packet is in the emulated switch sw1, and when rec.sw_id == 1 is the emulated switch sw2.
 - If you are in the sw1 switch, and want to forward the packet to the link h1 <--> sw1 you need to define the hdr.rec.sw = 0, and the ucast_egress_port = 132.
 - If you are in the sw1 switch, and want to forward the packet to the link sw1 <--> sw2 you need to define the hdr.rec.sw = 1, and the ucast_egress_port = 134.
 - If you are in the sw2 switch, and want to forward the packet to the link sw1 <--> sw2 you need to define the hdr.rec.sw = 1, and the ucast_egress_port = 134.
 - If you are in the sw2 switch, and want to forward the packet to the link sw2 <--> h2 you need to define the hdr.rec.sw = 2, and the ucast_egress_port = 140.

With this information you can create your table entries for your routing tables. In this example I have a table called "forwarding" that do match if the dst_ip, and then forward the packet.

So go back to main.py script and create the table entries similar to below:
```
# add table entry sw1
topo.addtable('sw1','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','132')
topo.addactionvalue('sw', '0')
topo.insert()

# add table entry sw1 (other direction)
topo.addtable('sw1','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','134')
topo.addactionvalue('sw', '1')
topo.insert()

# add table entry sw2
topo.addtable('sw2','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.10\')')
topo.addactionvalue('port','134')
topo.addactionvalue('sw', '1')
topo.insert()

# add table entry sw2 (other direction)
topo.addtable('sw2','SwitchIngress.forward')
topo.addaction('SwitchIngress.send')
topo.addmatch('dst_addr','IPAddress(\'192.168.0.20\')')
topo.addactionvalue('port','140')
topo.addactionvalue('sw', '2')
topo.insert()
```


After define your table entries properly (according to the P7 outputs and your tables in your p4 code), you can run the command below to start the execution:
```
python3 main.py -s
```
If is everything ok, you will be able to send traffic from/to your hosts :)

OBS: do not forget to use the p7 vlan in your packets.

## About P7
Options to validate a network topology, including the link metrics, are traditionally based on virtual environments (e.g., Mininet), limiting the experiments with transmission speeds over 10Gbps. By leveraging P4 programmability and new generation hardware, P7 comes as an alternative to define emulation characteristics of the links and represent a network topology with high fidelity and computation power using a single physical P4 switch (e.g., Tofino). It is possible to emulate network topologies using recirculations, port configurations, different match+action tables, and even DAC cables. What is more, we can connect physical servers to inject traffic to the topology.

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

**This is still a work in progress. Feedback is welcome!**

## Requirements

- git 
- python3
- matplotlib
- networkX
- regex
- polka-routing

**Necessary to run compile, run and set P4 code**

 - Stratum. *Please refer to the official building guide (https://github.com/stratum/stratum/blob/main/stratum/hal/bin/barefoot/README.build.md)*
 - P4Studio. *Tested with SDE 9.5+*

## Contributing
PRs are very much appreciated. For bugs/features consider creating an issue before sending a PR.

## Documentation
For further information, please read our wiki (https://github.com/intrig-unicamp/p7/wiki)

## Team
We are members of [INTRIG (Information & Networking Technologies Research & Innovation Group)](http://intrig.dca.fee.unicamp.br) at University of Campinas - Unicamp, SP, Brazil and [RNP (Rede Nacional de Ensino e Pesquisa)](https://www.rnp.br/).  

**P7 project was supported by and in technical collaboration with the Brazilian National Research and Education Network (RNP - Rede Nacional de Ensino e Pesquisa) (https://www.rnp.br/en)**  

Thanks to all [contributors](https://github.com/intrig-unicamp/p7/wiki#team)!
