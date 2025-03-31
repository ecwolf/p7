from netaddr import IPAddress
p4p7 = bfrt.p7_default.pipe_p7
p4user = bfrt.p7calc_mod.pipe
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
vlan_fwd.add_with_match(vid=1920, ingress_port=132,   link=0)

vlan_fwd = p4p7.SwitchIngress.vlan_fwd
vlan_fwd.add_with_match(vid=1920, ingress_port=134,   link=1)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=132,   link=0)

arp_fwd = p4p7.SwitchIngress.arp_fwd
arp_fwd.add_with_match_arp(vid=1920, ingress_port=134,   link=1)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=1, dest_ip=IPAddress('192.168.0.20'),   port=134)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=1, dest_ip=IPAddress('192.168.0.10'),   link_id=0, sw_id=0)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send(sw=0, dest_ip=IPAddress('192.168.0.10'),   port=132)

basic_fwd = p4p7.SwitchIngress.basic_fwd
basic_fwd.add_with_send_next(sw=0, dest_ip=IPAddress('192.168.0.20'),   link_id=1, sw_id=0)


tscal = p4p7.SwitchIngress.tscal
tscal.add(REGISTER_INDEX=0,f1=10000000)
tscal.add(REGISTER_INDEX=1,f1=0)

pkt_loss = p4p7.SwitchIngress.pkt_losscal
pkt_loss.add(REGISTER_INDEX=0,f1=102)
pkt_loss.add(REGISTER_INDEX=1,f1=0)

transition_state_p = p4p7.SwitchIngress.transition_state_p
transition_state_p.add(REGISTER_INDEX=0,f1=57)
transition_state_p.add(REGISTER_INDEX=1,f1=0)

transition_state_r = p4p7.SwitchIngress.transition_state_r
transition_state_r.add(REGISTER_INDEX=0,f1=510)
transition_state_r.add(REGISTER_INDEX=1,f1=0)

probability_send_k = p4p7.SwitchIngress.probability_send_k
probability_send_k.add(REGISTER_INDEX=0,f1=1020)
probability_send_k.add(REGISTER_INDEX=1,f1=1020)

probability_send_h = p4p7.SwitchIngress.probability_send_h
probability_send_h.add(REGISTER_INDEX=0,f1=0)
probability_send_h.add(REGISTER_INDEX=1,f1=0)

state_holder = p4p7.SwitchIngress.state
state_holder.add(REGISTER_INDEX=0,f1=1)
state_holder.add(REGISTER_INDEX=1,f1=1)

pkt_loss_model = p4p7.SwitchIngress.pkt_loss_model
pkt_loss_model.add(REGISTER_INDEX=0,f1=1)
pkt_loss_model.add(REGISTER_INDEX=1,f1=0)

calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 0, dst_addr = IPAddress('192.168.0.10'), value = 5)
calculate = p4user.SwitchIngress.calculate
calculate.add_with_operation_add(sw_id= 0, dst_addr = IPAddress('192.168.0.20'), value = 10)


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
print ("Table calculate:")
calculate.dump(table=True)
print ("Mirror:")
p4mirror.dump()
