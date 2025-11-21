from netaddr import IPAddress
p4p7 = bfrt.p7_default.pipe_p7
p4user0 = bfrt.simple_forward_mod.pipe
p4mirror = bfrt.mirror

def clear_all(verbose=True, batching=True):
    global p4p7
    global p4user0
    global bfrt

    for table_types in (['MATCH_DIRECT', 'MATCH_INDIRECT_SELECTOR'],
                        ['SELECTOR'],
                        ['ACTION_PROFILE']):
        for table in p4p7.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')
        for table in p4user0.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')

clear_all(verbose=True)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=164,   link=0, portRec=132)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=172,   link=13, portRec=136)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=164,   link=0, portRec=132)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=172,   link=13, portRec=136)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, sw_id=222, sw_id_next=0, portPipe=56, register_shift=0)
basic_fwd.add_with_send(sw=0, sw_id=0, port=164)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, sw_id=1, sw_id_next=0, portPipe=48, register_shift=0)
basic_fwd.add_with_send_next(sw=1, sw_id=0, sw_id_next=1, portPipe=48, register_shift=1000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, sw_id=2, sw_id_next=1, portPipe=40, register_shift=1000)
basic_fwd.add_with_send_next(sw=2, sw_id=1, sw_id_next=2, portPipe=40, register_shift=2000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, sw_id=3, sw_id_next=2, portPipe=32, register_shift=2000)
basic_fwd.add_with_send_next(sw=3, sw_id=2, sw_id_next=3, portPipe=32, register_shift=3000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, sw_id=4, sw_id_next=3, portPipe=24, register_shift=3000)
basic_fwd.add_with_send_next(sw=4, sw_id=3, sw_id_next=4, portPipe=24, register_shift=4000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=5, sw_id=5, sw_id_next=4, portPipe=16, register_shift=4000)
basic_fwd.add_with_send_next(sw=5, sw_id=4, sw_id_next=5, portPipe=16, register_shift=5000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=6, sw_id=6, sw_id_next=5, portPipe=8, register_shift=5000)
basic_fwd.add_with_send_next(sw=6, sw_id=5, sw_id_next=6, portPipe=8, register_shift=6000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=7, sw_id=7, sw_id_next=6, portPipe=0, register_shift=6000)
basic_fwd.add_with_send_next(sw=7, sw_id=6, sw_id_next=7, portPipe=0, register_shift=7000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=8, sw_id=8, sw_id_next=7, portPipe=4, register_shift=7000)
basic_fwd.add_with_send_next(sw=8, sw_id=7, sw_id_next=8, portPipe=4, register_shift=8000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=9, sw_id=9, sw_id_next=8, portPipe=12, register_shift=8000)
basic_fwd.add_with_send_next(sw=9, sw_id=8, sw_id_next=9, portPipe=12, register_shift=9000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=10, sw_id=10, sw_id_next=9, portPipe=20, register_shift=9000)
basic_fwd.add_with_send_next(sw=10, sw_id=9, sw_id_next=10, portPipe=20, register_shift=10000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=11, sw_id=11, sw_id_next=10, portPipe=28, register_shift=10000)
basic_fwd.add_with_send_next(sw=11, sw_id=10, sw_id_next=11, portPipe=28, register_shift=11000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=12, sw_id=12, sw_id_next=11, portPipe=36, register_shift=11000)
basic_fwd.add_with_send_next(sw=12, sw_id=11, sw_id_next=12, portPipe=36, register_shift=12000)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=13, sw_id=222, sw_id_next=12, portPipe=44, register_shift=12000)
basic_fwd.add_with_send(sw=13, sw_id=12, port=172)

tscal = p4p7.SwitchIngress.tscal
tscal.add(REGISTER_INDEX=0,f1=0)
tscal.add(REGISTER_INDEX=1,f1=0)
tscal.add(REGISTER_INDEX=2,f1=0)
tscal.add(REGISTER_INDEX=3,f1=0)
tscal.add(REGISTER_INDEX=4,f1=0)
tscal.add(REGISTER_INDEX=5,f1=0)
tscal.add(REGISTER_INDEX=6,f1=0)
tscal.add(REGISTER_INDEX=7,f1=0)
tscal.add(REGISTER_INDEX=8,f1=0)
tscal.add(REGISTER_INDEX=9,f1=0)
tscal.add(REGISTER_INDEX=10,f1=0)
tscal.add(REGISTER_INDEX=11,f1=0)
tscal.add(REGISTER_INDEX=12,f1=0)
tscal.add(REGISTER_INDEX=13,f1=0)

pkt_loss = p4p7.SwitchIngress.pkt_losscal
pkt_loss.add(REGISTER_INDEX=0,f1=0)
pkt_loss.add(REGISTER_INDEX=1,f1=0)
pkt_loss.add(REGISTER_INDEX=2,f1=0)
pkt_loss.add(REGISTER_INDEX=3,f1=0)
pkt_loss.add(REGISTER_INDEX=4,f1=0)
pkt_loss.add(REGISTER_INDEX=5,f1=0)
pkt_loss.add(REGISTER_INDEX=6,f1=0)
pkt_loss.add(REGISTER_INDEX=7,f1=0)
pkt_loss.add(REGISTER_INDEX=8,f1=0)
pkt_loss.add(REGISTER_INDEX=9,f1=0)
pkt_loss.add(REGISTER_INDEX=10,f1=0)
pkt_loss.add(REGISTER_INDEX=11,f1=0)
pkt_loss.add(REGISTER_INDEX=12,f1=0)
pkt_loss.add(REGISTER_INDEX=13,f1=0)

transition_state_p = p4p7.SwitchIngress.transition_state_p
transition_state_p.add(REGISTER_INDEX=0,f1=0)
transition_state_p.add(REGISTER_INDEX=1,f1=0)
transition_state_p.add(REGISTER_INDEX=2,f1=0)
transition_state_p.add(REGISTER_INDEX=3,f1=0)
transition_state_p.add(REGISTER_INDEX=4,f1=0)
transition_state_p.add(REGISTER_INDEX=5,f1=0)
transition_state_p.add(REGISTER_INDEX=6,f1=0)
transition_state_p.add(REGISTER_INDEX=7,f1=0)
transition_state_p.add(REGISTER_INDEX=8,f1=0)
transition_state_p.add(REGISTER_INDEX=9,f1=0)
transition_state_p.add(REGISTER_INDEX=10,f1=0)
transition_state_p.add(REGISTER_INDEX=11,f1=0)
transition_state_p.add(REGISTER_INDEX=12,f1=0)
transition_state_p.add(REGISTER_INDEX=13,f1=0)

transition_state_r = p4p7.SwitchIngress.transition_state_r
transition_state_r.add(REGISTER_INDEX=0,f1=0)
transition_state_r.add(REGISTER_INDEX=1,f1=0)
transition_state_r.add(REGISTER_INDEX=2,f1=0)
transition_state_r.add(REGISTER_INDEX=3,f1=0)
transition_state_r.add(REGISTER_INDEX=4,f1=0)
transition_state_r.add(REGISTER_INDEX=5,f1=0)
transition_state_r.add(REGISTER_INDEX=6,f1=0)
transition_state_r.add(REGISTER_INDEX=7,f1=0)
transition_state_r.add(REGISTER_INDEX=8,f1=0)
transition_state_r.add(REGISTER_INDEX=9,f1=0)
transition_state_r.add(REGISTER_INDEX=10,f1=0)
transition_state_r.add(REGISTER_INDEX=11,f1=0)
transition_state_r.add(REGISTER_INDEX=12,f1=0)
transition_state_r.add(REGISTER_INDEX=13,f1=0)

probability_send_k = p4p7.SwitchIngress.probability_send_k
probability_send_k.add(REGISTER_INDEX=0,f1=1020)
probability_send_k.add(REGISTER_INDEX=1,f1=1020)
probability_send_k.add(REGISTER_INDEX=2,f1=1020)
probability_send_k.add(REGISTER_INDEX=3,f1=1020)
probability_send_k.add(REGISTER_INDEX=4,f1=1020)
probability_send_k.add(REGISTER_INDEX=5,f1=1020)
probability_send_k.add(REGISTER_INDEX=6,f1=1020)
probability_send_k.add(REGISTER_INDEX=7,f1=1020)
probability_send_k.add(REGISTER_INDEX=8,f1=1020)
probability_send_k.add(REGISTER_INDEX=9,f1=1020)
probability_send_k.add(REGISTER_INDEX=10,f1=1020)
probability_send_k.add(REGISTER_INDEX=11,f1=1020)
probability_send_k.add(REGISTER_INDEX=12,f1=1020)
probability_send_k.add(REGISTER_INDEX=13,f1=1020)

probability_send_h = p4p7.SwitchIngress.probability_send_h
probability_send_h.add(REGISTER_INDEX=0,f1=0)
probability_send_h.add(REGISTER_INDEX=1,f1=0)
probability_send_h.add(REGISTER_INDEX=2,f1=0)
probability_send_h.add(REGISTER_INDEX=3,f1=0)
probability_send_h.add(REGISTER_INDEX=4,f1=0)
probability_send_h.add(REGISTER_INDEX=5,f1=0)
probability_send_h.add(REGISTER_INDEX=6,f1=0)
probability_send_h.add(REGISTER_INDEX=7,f1=0)
probability_send_h.add(REGISTER_INDEX=8,f1=0)
probability_send_h.add(REGISTER_INDEX=9,f1=0)
probability_send_h.add(REGISTER_INDEX=10,f1=0)
probability_send_h.add(REGISTER_INDEX=11,f1=0)
probability_send_h.add(REGISTER_INDEX=12,f1=0)
probability_send_h.add(REGISTER_INDEX=13,f1=0)

state_holder = p4p7.SwitchIngress.state
state_holder.add(REGISTER_INDEX=0,f1=1)
state_holder.add(REGISTER_INDEX=1,f1=1)
state_holder.add(REGISTER_INDEX=2,f1=1)
state_holder.add(REGISTER_INDEX=3,f1=1)
state_holder.add(REGISTER_INDEX=4,f1=1)
state_holder.add(REGISTER_INDEX=5,f1=1)
state_holder.add(REGISTER_INDEX=6,f1=1)
state_holder.add(REGISTER_INDEX=7,f1=1)
state_holder.add(REGISTER_INDEX=8,f1=1)
state_holder.add(REGISTER_INDEX=9,f1=1)
state_holder.add(REGISTER_INDEX=10,f1=1)
state_holder.add(REGISTER_INDEX=11,f1=1)
state_holder.add(REGISTER_INDEX=12,f1=1)
state_holder.add(REGISTER_INDEX=13,f1=1)

pkt_loss_model = p4p7.SwitchIngress.pkt_loss_model
pkt_loss_model.add(REGISTER_INDEX=0,f1=0)
pkt_loss_model.add(REGISTER_INDEX=1,f1=0)
pkt_loss_model.add(REGISTER_INDEX=2,f1=0)
pkt_loss_model.add(REGISTER_INDEX=3,f1=0)
pkt_loss_model.add(REGISTER_INDEX=4,f1=0)
pkt_loss_model.add(REGISTER_INDEX=5,f1=0)
pkt_loss_model.add(REGISTER_INDEX=6,f1=0)
pkt_loss_model.add(REGISTER_INDEX=7,f1=0)
pkt_loss_model.add(REGISTER_INDEX=8,f1=0)
pkt_loss_model.add(REGISTER_INDEX=9,f1=0)
pkt_loss_model.add(REGISTER_INDEX=10,f1=0)
pkt_loss_model.add(REGISTER_INDEX=11,f1=0)
pkt_loss_model.add(REGISTER_INDEX=12,f1=0)
pkt_loss_model.add(REGISTER_INDEX=13,f1=0)

forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 0, dst_addr = IPAddress('192.168.0.20'), port = 140, sw = 1)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 0, dst_addr = IPAddress('192.168.0.10'), port = 132, sw = 0)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 1, dst_addr = IPAddress('192.168.0.20'), port = 148, sw = 2)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 1, dst_addr = IPAddress('192.168.0.10'), port = 140, sw = 1)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 2, dst_addr = IPAddress('192.168.0.20'), port = 156, sw = 3)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 2, dst_addr = IPAddress('192.168.0.10'), port = 148, sw = 2)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 3, dst_addr = IPAddress('192.168.0.20'), port = 180, sw = 4)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 3, dst_addr = IPAddress('192.168.0.10'), port = 156, sw = 3)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 4, dst_addr = IPAddress('192.168.0.20'), port = 188, sw = 5)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 4, dst_addr = IPAddress('192.168.0.10'), port = 180, sw = 4)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 5, dst_addr = IPAddress('192.168.0.20'), port = 184, sw = 6)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 5, dst_addr = IPAddress('192.168.0.10'), port = 188, sw = 5)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 6, dst_addr = IPAddress('192.168.0.20'), port = 176, sw = 7)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 6, dst_addr = IPAddress('192.168.0.10'), port = 184, sw = 6)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 7, dst_addr = IPAddress('192.168.0.20'), port = 168, sw = 8)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 7, dst_addr = IPAddress('192.168.0.10'), port = 176, sw = 7)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 8, dst_addr = IPAddress('192.168.0.20'), port = 160, sw = 9)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 8, dst_addr = IPAddress('192.168.0.10'), port = 168, sw = 8)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 9, dst_addr = IPAddress('192.168.0.20'), port = 144, sw = 10)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 9, dst_addr = IPAddress('192.168.0.10'), port = 160, sw = 9)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 10, dst_addr = IPAddress('192.168.0.20'), port = 152, sw = 11)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 10, dst_addr = IPAddress('192.168.0.10'), port = 144, sw = 10)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 11, dst_addr = IPAddress('192.168.0.20'), port = 128, sw = 12)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 11, dst_addr = IPAddress('192.168.0.10'), port = 152, sw = 11)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 12, dst_addr = IPAddress('192.168.0.20'), port = 136, sw = 13)
forward = p4user0.SwitchIngress.forward
forward.add_with_send(sw_id= 12, dst_addr = IPAddress('192.168.0.10'), port = 128, sw = 12)


bfrt.complete_operations()

print("""
******************* PROGAMMING RESULTS *****************
""")
print ("Table vlan_fwd:")
vlan_fwd.dump(table=True)
print ("Table arp_fwd:")
arp_fwd.dump(table=True)
print ("Table basic_fwd:")
basic_fwd.dump(table=True)
print ("Table forward:")
forward.dump(table=True)
print ("Mirror:")
p4mirror.dump()
