/*******************************************************************************
 * Copyright 2025 INTRIG
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 ******************************************************************************/

#include <tna.p4>

#include "common/headers.p4"
#include "common/util.p4"

/*************************************************************************
 ************* C O N S T A N T S    A N D   T Y P E S  *******************
**************************************************************************/
const vlan_id_t p7_vlan = 1920;        // vlan for P7
const PortId_t rec_port = 196;       // recirculation port
const PortId_t port_user = 68;       // recirculation port
const bit<32> constJitter = 0;   // jitter  - 0 - 0ms
const bit<7> percentTax = 127;   // percent*127/100
const bit<16> maxPercent = 0x3fc;	// Not used, but is the representation of 100% value

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

/***********************  H E A D E R S  ************************/

struct my_ingress_metadata_t {
    bit<32>  ts_diff;
    bit<32>  jitter_metadata;
    bit<1>   signal_metadata;
    bit<31>  padding;
    bit<16>  R;
    bit<1>   prob_r;
    bit<1>   prob_p;
    bit<14>  padd;
}

    /******  G L O B A L   I N G R E S S   M E T A D A T A  *********/

parser SwitchIngressParser(
       packet_in packet, 
       out headers hdr, 
       out my_ingress_metadata_t md,
       out ingress_intrinsic_metadata_t ig_intr_md) {

    state start {
        packet.extract(ig_intr_md);
        packet.advance(PORT_METADATA_SIZE);
        transition parse_ethernet;
    }

    state parse_ethernet {
        packet.extract(hdr.ethernet);
        transition select(hdr.ethernet.ether_type) {
            ETHERTYPE_ARP:  parse_arp;
            ETHERTYPE_IPV4:  parse_ipv4;
            ETHERTYPE_VLAN:  parse_vlan;
            ETHERTYPE_REC:   parse_rec;   // Recirculation header
            default: accept;
        }
    }

    state parse_vlan {
        packet.extract(hdr.vlan_tag);
        transition select(hdr.vlan_tag.ether_type) {
            ETHERTYPE_ARP:  parse_arp;
            ETHERTYPE_IPV4:  parse_ipv4;
            default: accept;
        }
    }

    state parse_arp {
        packet.extract(hdr.arp);
        transition accept;
    }

    state parse_ipv4 {
        packet.extract(hdr.ipv4);
        transition accept;
    }

    state parse_rec {
        packet.extract(hdr.rec);
        transition parse_vlan;
    }
}

control SwitchIngressDeparser(
        packet_out pkt,
        inout headers hdr,
        in my_ingress_metadata_t ig_md,
        in ingress_intrinsic_metadata_for_deparser_t ig_intr_dprsr_md) {

    apply {
        pkt.emit(hdr);
    }
}

control SwitchIngress(
        inout headers hdr, 
        inout my_ingress_metadata_t md,
        in ingress_intrinsic_metadata_t ig_intr_md,
        in ingress_intrinsic_metadata_from_parser_t ig_intr_prsr_md,
        inout ingress_intrinsic_metadata_for_deparser_t ig_intr_dprsr_md,
        inout ingress_intrinsic_metadata_for_tm_t ig_intr_tm_md) {

    // Random value used to calculate pkt loss jitter
    Random<bit<10>>() rnd;
    Random<bit<7>>() percent;
    Random<bit<1>>() signalSelector;

    // Register to validate the latency value
    Register <bit<32>, bit<16>> (32w1024)  tscal;
    
    // Register to validate the Jitter value
    Register <bit<32>, _> (32w1)  ax;

    //Register to valdiate the packet loss model
    Register <bit<16>, bit<16>> (32w1024)  pkt_losscal;
    Register <bit<32>, bit<16>> (32w1024)  transition_state;
    Register <bit<32>, bit<16>> (32w1024)  probability_send;
    Register <bit<1>, bit<16>> (32w1024) state;
    Register <bit<8>, bit<16>> (32w1024) pkt_loss_model;

    RegisterAction<bit<32>, bit<16>, bit<8>>(tscal) tscal_action = {
        void apply(inout bit<32> latency, out bit<8> readvalue){
            if (md.ts_diff > latency){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<16>, bit<16>, bit<8>>(pkt_losscal) pkt_loss_action = {
        void apply(inout bit<16> pkt_loss, out bit<8> readvalue){
            if (md.R >= pkt_loss){ // @1-pkt_loss
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(ax) ax_action = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > constJitter){ // @jitter
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<8>, bit<16>, bit<8>>(pkt_loss_model) pkt_loss_model_action = {
        void apply(inout bit<8> loss_model, out bit<8> readvalue){
            readvalue = loss_model;
        }
    };

    RegisterAction<bit<32>, bit<16>, bit<32>>(transition_state) transition_state_action = {
        void apply(inout bit<32> probability, out bit<32> readvalue){
            readvalue = probability;
        }
    };

    RegisterAction<bit<32>, bit<16>, bit<32>>(probability_send) probability_send_action = {
        void apply(inout bit<32> probability, out bit<32> readvalue){
            readvalue = probability;
        }
    };

    RegisterAction<bit<1>, bit<16>, bit<1>>(state) state_action = {
        void apply(inout bit<1> state_value, out bit<1> readvalue){
			if (state_value == 1){   // GOOD_CASE - apply p condition
				state_value = md.prob_p;
			}else {                    // BAD_CASE - apply r condition
				state_value = md.prob_r;
			}
			readvalue = state_value;
        }
    };

    action drop() {
        ig_intr_dprsr_md.drop_ctl = 0x1;
    }

    // Send the packet to output port
    // Remove the recirculation header
    // Set back the ethertype of the original packet
    action send(PortId_t port) {
        //hdr.ethernet.src_addr[31:0] = hdr.rec.num;
        hdr.ethernet.ether_type = hdr.rec.ether_type;
        ig_intr_tm_md.ucast_egress_port = port;
        hdr.rec.setInvalid();
        ig_intr_tm_md.bypass_egress = 1w1;
    }

    // Send packet to the next internal switch 
    // Reset the initial timestamp
    // Increase the ID of the switch
    action send_next(bit<16> link_id, bit<16> sw_id) {
        hdr.rec.ts = ig_intr_md.ingress_mac_tstamp[31:0];
        hdr.rec.num = 1;

        hdr.rec.sw = link_id;
        hdr.rec.sw_id = sw_id;

        ig_intr_tm_md.ucast_egress_port = port_user;
    }

    // Forward a packet directly without any P7 processing
    action send_direct(PortId_t port) {
        ig_intr_tm_md.ucast_egress_port = port;
    }

    // Recirculate the packet to the recirculation port
    // Increase the recirculation number
    action recirculate(PortId_t recirc_port){
        ig_intr_tm_md.ucast_egress_port = recirc_port;
        hdr.rec.num = hdr.rec.num + 1;      // using new header
    }

    // Calculate the difference between the initial timestamp a the current timestamp
    action comp_diff() {
        md.ts_diff = ig_intr_md.ingress_mac_tstamp[31:0] - hdr.rec.ts;
    }

    // increases jitter in the timestamp difference
    action apply_more_jitter(){
	 	md.ts_diff = md.ts_diff + hdr.rec.jitter;
    }

    // decreases jitter in the timestamp difference
    action apply_less_jitter(){
    	md.ts_diff = md.ts_diff - hdr.rec.jitter;
    }

    // Match incoming packet
    // Add recirculation header
    // Save the ethertype of the original packet in the recirculation header - ether_type
    // Save the initial timestamp (ingress_mac_tstamp) in the recirculation header - ts
    // Set the starting number of recirculation - num
    // Set the ID of the first switch - sw
    action match(bit<16> link) {
        hdr.rec.setValid();
        hdr.rec.ts = ig_intr_md.ingress_mac_tstamp[31:0];
        hdr.rec.num = 1;
        hdr.rec.sw = link;
        hdr.rec.dest_ip = hdr.ipv4.dst_addr;
        hdr.rec.ether_type = hdr.ethernet.ether_type;
        hdr.vlan_tag.vid = p7_vlan;

        hdr.rec.jitter = md.jitter_metadata;
        hdr.rec.signal = md.signal_metadata;

        hdr.ethernet.ether_type = 0x9966;

        ig_intr_tm_md.ucast_egress_port = rec_port;
        ig_intr_tm_md.bypass_egress = 1w1;
    }

    action match_arp(bit<16> link) {
        hdr.rec.setValid();
        hdr.rec.ts = ig_intr_md.ingress_mac_tstamp[31:0];
        hdr.rec.num = 1;
        hdr.rec.sw = link;
        hdr.rec.dest_ip = hdr.arp.dest_ip;
        hdr.rec.ether_type = hdr.ethernet.ether_type;
        hdr.vlan_tag.vid = p7_vlan;

        hdr.rec.jitter = md.jitter_metadata;
        hdr.rec.signal = md.signal_metadata;

        hdr.ethernet.ether_type = 0x9966;

        ig_intr_tm_md.ucast_egress_port = rec_port;
        ig_intr_tm_md.bypass_egress = 1w1;
    }

    action match_arp_direct(PortId_t port) {
        ig_intr_tm_md.ucast_egress_port = port;
    }

    // Table perform l2 forward
    // Match the interconnection ID and the destination IP
    table basic_fwd {
        key = {
            hdr.rec.sw : exact;
            hdr.rec.dest_ip   : exact;
        }
        actions = {
            send_next;
            send;
            @defaultonly drop;
        }
        const default_action = drop();
        size = 128;
    }


    // Table to verify the VLAN_ID to be processed by P7
    // Match the VLAN_ID and the ingress port
    table vlan_fwd {
        key = {
            hdr.vlan_tag.vid   : exact;
            ig_intr_md.ingress_port : exact;
        }
        actions = {
            send_direct;
            match;
            @defaultonly drop;
        }
        const default_action = drop();
        size = 128;
    }

    table arp_fwd {
        key = {
            hdr.vlan_tag.vid   : exact;
            ig_intr_md.ingress_port : exact;
        }
        actions = {
            match_arp;
            match_arp_direct;
            @defaultonly drop;
        }
        const default_action = drop();
        size = 128;
    }


    apply {
        //sets the jitter to be applied
	 	if(!hdr.rec.isValid()){
	    	bit<7> P = percent.get();
	    	if(P <= percentTax){
	        	md.jitter_metadata = constJitter;
				md.signal_metadata = signalSelector.get();
	    	}
	    	else{
				md.jitter_metadata = 0;
				md.signal_metadata = 0;
	    	}
	  	}
	  	
        // Validate if the incoming packet has VLAN header
        // Match the VLAN_ID with P7
        if (hdr.vlan_tag.isValid() && !hdr.rec.isValid() && !hdr.arp.isValid()) {
       	 	vlan_fwd.apply();
        }
        else if (hdr.vlan_tag.isValid() && !hdr.rec.isValid() && hdr.arp.isValid()) {
        	arp_fwd.apply();
        } else {
            // If the recirculation header is valid, match the switch ID
            // Then verify the timestamp difference (latency)
            // Apply the packet_loss value with the random number generated
            // Verify if the switch is the final one or need to be processed by the next one
            if (hdr.rec.isValid()) {
                    bit<16> select_sw = hdr.rec.sw;
                    md.ts_diff = 0;
                    comp_diff();
    		     	//apply the jitter
		     		if(hdr.rec.signal==0){
		         		apply_more_jitter();
      		     	}else{
   		         		if(ax_action.execute(1)==1)
		     	     		apply_less_jitter();
		     		 	}
                    if (tscal_action.execute(select_sw) == 1){
                        md.R = (bit<16>)rnd.get();
                        if (gilbert == 1){
                            bit<16> R_send= (bit<16>)rnd.get();
                            bit<32> global_probability = transition_state_action.execute(select_sw);
                            bit<16> p = global_probability[31:16];
                            bit<16> r = global_probability[15:0];
                            bit<32> send_probability = probability_send_action.execute(select_sw);
                            bit<16> h = send_probability[31:16];
                            bit<16> k = send_probability[15:0];                        
                            bit<1> value_state;
                            if ( p > md.R ) {  // if p > R, go to bad state
                                md.prob_p = 0;
                            }else {         // else p < R, keep to good state
                                md.prob_p = 1;
                            }

                            if ( r > md.R ) {  // if r > R, go to good state
                                md.prob_r = 1;
                            }else {         // else r < R, keep to bad stae
                                md.prob_r = 0;
                            }
                            value_state = state_action.execute(select_sw); // change state according md.prob_p or md.prob_r
                            if ( value_state == 1) {
                                if ( R_send < maxPercent - k ) {
                                    drop();
                                } else {
                                    basic_fwd.apply();
                                }
                            } else {
                                if ( h > R_send ) {
                                    basic_fwd.apply();
                                } else {
                                    drop();
                                }
                            }
                        }else{
                            if (pkt_loss_action.execute(select_sw) == 1) {            // @2-% of pkt loss 
                                basic_fwd.apply();
                            }else{
                                drop();
                            } 
                        }
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
            // If the recirculation header is not valid
            // Perform the match action to add recirculation header           
            }else{
               drop();    
            }
        }
        // No need for egress processing, skip it and use empty controls for egress.
        ig_intr_tm_md.bypass_egress = 1w1;
    }
}

Pipeline(SwitchIngressParser(),
         SwitchIngress(),
         SwitchIngressDeparser(),
         EmptyEgressParser(),
         EmptyEgress(),
         EmptyEgressDeparser()) pipe_p7;

Switch(pipe_p7) main;
