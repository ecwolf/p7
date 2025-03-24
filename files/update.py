from netaddr import IPAddress
p4p7 = bfrt.p7_default.pipe_p7
p4user = bfrt.p7calc_mod.pipe
p4mirror = bfrt.mirror

tscal = p4p7.SwitchIngress.tscal
tscal.add(REGISTER_INDEX=0,f1=10000000)
tscal.add(REGISTER_INDEX=1,f1=0)

pkt_loss = p4p7.SwitchIngress.pkt_losscal
pkt_loss.add(REGISTER_INDEX=0,f1=102)
pkt_loss.add(REGISTER_INDEX=1,f1=0)

bfrt.complete_operations()


