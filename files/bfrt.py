from netaddr import IPAddress
p4p7 = bfrt.p7_default.pipe_p7
p4user = bfrt.simple_forward_mod.pipe
p4mirror = bfrt.mirror

def clear_all(verbose=True, batching=True):
    global p4p7
    global p4user
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
        for table in p4user.info(return_info=True, print_info=False):
            if table['type'] in table_types:
                if verbose:
                    print("Clearing table {:<40} ... ".
                          format(table['full_name']), end='', flush=True)
                table['node'].clear(batch=batching)
                if verbose:
                    print('Done')

clear_all(verbose=True)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=135,   link=0, portRec=140)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=133,   link=13, portRec=128)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=135,   link=0, portRec=140)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=133,   link=13, portRec=128)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, sw_id=222, sw_id_next=0, portPipe=56)
basic_fwd.add_with_send(sw=0, sw_id=0, port=135)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, sw_id=1, sw_id_next=0, portPipe=48)
basic_fwd.add_with_send_next(sw=1, sw_id=0, sw_id_next=1, portPipe=48)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=2, sw_id=2, sw_id_next=1, portPipe=40)
basic_fwd.add_with_send_next(sw=2, sw_id=1, sw_id_next=2, portPipe=40)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=3, sw_id=3, sw_id_next=2, portPipe=32)
basic_fwd.add_with_send_next(sw=3, sw_id=2, sw_id_next=3, portPipe=32)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=4, sw_id=4, sw_id_next=3, portPipe=24)
basic_fwd.add_with_send_next(sw=4, sw_id=3, sw_id_next=4, portPipe=24)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=5, sw_id=5, sw_id_next=4, portPipe=16)
basic_fwd.add_with_send_next(sw=5, sw_id=4, sw_id_next=5, portPipe=16)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=6, sw_id=6, sw_id_next=5, portPipe=8)
basic_fwd.add_with_send_next(sw=6, sw_id=5, sw_id_next=6, portPipe=8)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=7, sw_id=7, sw_id_next=6, portPipe=0)
basic_fwd.add_with_send_next(sw=7, sw_id=6, sw_id_next=7, portPipe=0)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=8, sw_id=8, sw_id_next=7, portPipe=4)
basic_fwd.add_with_send_next(sw=8, sw_id=7, sw_id_next=8, portPipe=4)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=9, sw_id=9, sw_id_next=8, portPipe=12)
basic_fwd.add_with_send_next(sw=9, sw_id=8, sw_id_next=9, portPipe=12)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=10, sw_id=10, sw_id_next=9, portPipe=20)
basic_fwd.add_with_send_next(sw=10, sw_id=9, sw_id_next=10, portPipe=20)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=11, sw_id=11, sw_id_next=10, portPipe=28)
basic_fwd.add_with_send_next(sw=11, sw_id=10, sw_id_next=11, portPipe=28)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=12, sw_id=12, sw_id_next=11, portPipe=36)
basic_fwd.add_with_send_next(sw=12, sw_id=11, sw_id_next=12, portPipe=36)
basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=13, sw_id=222, sw_id_next=12, portPipe=44)
basic_fwd.add_with_send(sw=13, sw_id=12, port=133)

tscal = p4p7.SwitchIngress.tscal
tscal.add(REGISTER_INDEX=0,f1=10000000)
tscal.add(REGISTER_INDEX=1,f1=10000000)
tscal.add(REGISTER_INDEX=2,f1=10000000)
tscal.add(REGISTER_INDEX=3,f1=10000000)
tscal.add(REGISTER_INDEX=4,f1=10000000)
tscal.add(REGISTER_INDEX=5,f1=10000000)
tscal.add(REGISTER_INDEX=6,f1=10000000)
tscal.add(REGISTER_INDEX=7,f1=10000000)
tscal.add(REGISTER_INDEX=8,f1=10000000)
tscal.add(REGISTER_INDEX=9,f1=10000000)
tscal.add(REGISTER_INDEX=10,f1=10000000)
tscal.add(REGISTER_INDEX=11,f1=10000000)
tscal.add(REGISTER_INDEX=12,f1=10000000)
tscal.add(REGISTER_INDEX=13,f1=10000000)

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

forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 0, dst_addr = IPAddress('192.168.0.20'), port = 148, sw = 1)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 0, dst_addr = IPAddress('192.168.0.10'), port = 140, sw = 0)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 1, dst_addr = IPAddress('192.168.0.20'), port = 156, sw = 2)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 1, dst_addr = IPAddress('192.168.0.10'), port = 148, sw = 1)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 2, dst_addr = IPAddress('192.168.0.20'), port = 164, sw = 3)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 2, dst_addr = IPAddress('192.168.0.10'), port = 156, sw = 2)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 3, dst_addr = IPAddress('192.168.0.20'), port = 172, sw = 4)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 3, dst_addr = IPAddress('192.168.0.10'), port = 164, sw = 3)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 4, dst_addr = IPAddress('192.168.0.20'), port = 180, sw = 5)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 4, dst_addr = IPAddress('192.168.0.10'), port = 172, sw = 4)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 5, dst_addr = IPAddress('192.168.0.20'), port = 188, sw = 6)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 5, dst_addr = IPAddress('192.168.0.10'), port = 180, sw = 5)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 6, dst_addr = IPAddress('192.168.0.20'), port = 184, sw = 7)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 6, dst_addr = IPAddress('192.168.0.10'), port = 188, sw = 6)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 7, dst_addr = IPAddress('192.168.0.20'), port = 176, sw = 8)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 7, dst_addr = IPAddress('192.168.0.10'), port = 184, sw = 7)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 8, dst_addr = IPAddress('192.168.0.20'), port = 168, sw = 9)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 8, dst_addr = IPAddress('192.168.0.10'), port = 176, sw = 8)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 9, dst_addr = IPAddress('192.168.0.20'), port = 160, sw = 10)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 9, dst_addr = IPAddress('192.168.0.10'), port = 168, sw = 9)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 10, dst_addr = IPAddress('192.168.0.20'), port = 144, sw = 11)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 10, dst_addr = IPAddress('192.168.0.10'), port = 160, sw = 10)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 11, dst_addr = IPAddress('192.168.0.20'), port = 152, sw = 12)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 11, dst_addr = IPAddress('192.168.0.10'), port = 144, sw = 11)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 12, dst_addr = IPAddress('192.168.0.20'), port = 128, sw = 13)
forward = p4user.SwitchIngress.forward
forward.add_with_send(sw_id= 12, dst_addr = IPAddress('192.168.0.10'), port = 152, sw = 12)


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
