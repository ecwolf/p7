/*******************************************************************************
 * Copyright 2024 INTRIG
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
const bit<16> total_sw = 6;         // total number of switches
const bit<10> pkt_loss0 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss1 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss2 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss3 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss4 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss5 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss6 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss7 = 0x0;       // packet loss  - 0%
const bit<10> pkt_loss8 = 0x0;       // packet loss  - 0%
const PortId_t rec_port = 196;       // recirculation port
const PortId_t port_user = 68;       // recirculation port
const bit<32> latency0 = 0;   // latency0  - 0 - 0ms
const bit<32> latency1 = 0;   // latency1  - 0 - 0ms
const bit<32> latency2 = 0;   // latency2  - 0 - 0ms
const bit<32> latency3 = 0;   // latency3  - 0 - 0ms
const bit<32> latency4 = 0;   // latency4  - 0 - 0ms
const bit<32> latency5 = 0;   // latency5  - 0 - 0ms
const bit<32> latency6 = 0;   // latency6  - 0 - 0ms
const bit<32> latency7 = 0;   // latency7  - 0 - 0ms
const bit<32> latency8 = 0;   // latency8  - 0 - 0ms
const bit<32> constJitter = 0;   // jitter  - 0 - 0ms
const bit<7> percentTax = 127;   // percent*127/100

/*************************************************************************
**************  I N G R E S S   P R O C E S S I N G   *******************
*************************************************************************/

/***********************  H E A D E R S  ************************/

struct my_ingress_metadata_t {
    bit<32>  ts_diff;
    bit<32>  jitter_metadata;
    bit<1>   signal_metadata;
    bit<31>  padding;

    // PolKa
    bit<152> ndata;
    bit<8> diff;
    bit<8> nres;
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
        transition select(hdr.ipv4.protocol) {
            IP_PROTOCOLS_TCP: parse_tcp;
            IP_PROTOCOLS_UDP: parse_udp;
            default: accept;
        }
    }

    state parse_tcp {
        packet.extract(hdr.tcp);
        transition accept;
    }

    state parse_udp {
        packet.extract(hdr.udp);
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

    // PolKa routing
    CRCPolynomial<bit<8>>(
                            coeff    = (285 & 0xff),
                            reversed = false,
                            msb      = false,
                            extended = false,
                            init     = 8w0x00,
                            xor      = 8w0x00) poly2;
    Hash<bit<8>>(HashAlgorithm_t.CUSTOM, poly2) hash2;

    CRCPolynomial<bit<8>>(
                            coeff    = (299 & 0xff),
                            reversed = false,
                            msb      = false,
                            extended = false,
                            init     = 8w0x00,
                            xor      = 8w0x00) poly3;
    Hash<bit<8>>(HashAlgorithm_t.CUSTOM, poly3) hash3;

    CRCPolynomial<bit<8>>(
                            coeff    = (301 & 0xff),
                            reversed = false,
                            msb      = false,
                            extended = false,
                            init     = 8w0x00,
                            xor      = 8w0x00) poly4;
    Hash<bit<8>>(HashAlgorithm_t.CUSTOM, poly4) hash4;

    CRCPolynomial<bit<8>>(
                            coeff    = (313 & 0xff),
                            reversed = false,
                            msb      = false,
                            extended = false,
                            init     = 8w0x00,
                            xor      = 8w0x00) poly5;
    Hash<bit<8>>(HashAlgorithm_t.CUSTOM, poly5) hash5;

    // Random value used to calculate pkt loss jitter
    Random<bit<10>>() rnd;
    Random<bit<7>>() percent;
    Random<bit<1>>() signalSelector;

    // Register to validate the latency value
    Register <bit<32>, _> (32w1)  tscal0;
    Register <bit<32>, _> (32w1)  tscal1;
    Register <bit<32>, _> (32w1)  tscal2;
    Register <bit<32>, _> (32w1)  tscal3;
    Register <bit<32>, _> (32w1)  tscal4;
    Register <bit<32>, _> (32w1)  tscal5;
    Register <bit<32>, _> (32w1)  tscal6;
    Register <bit<32>, _> (32w1)  tscal7;
    Register <bit<32>, _> (32w1)  tscal8;
    Register <bit<32>, _> (32w1)  ax;

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal0) tscal_action0 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency0){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal1) tscal_action1 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency1){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal2) tscal_action2 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency2){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal3) tscal_action3 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency3){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal4) tscal_action4 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency4){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal5) tscal_action5 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency5){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal6) tscal_action6 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency6){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal7) tscal_action7 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency7){ // @1-latency
                readvalue = 1;
            }else {
                readvalue = 0;
            }
        }
    };

    RegisterAction<bit<32>, bit<1>, bit<8>>(tscal8) tscal_action8 = {
        void apply(inout bit<32> value, out bit<8> readvalue){
            value = 0;
            if (md.ts_diff > latency8){ // @1-latency
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

    action drop() {
        ig_intr_dprsr_md.drop_ctl = 0x1;
    }

    action NoAction(){}

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
    action send_next(bit<16> sw_id) {
        // PolKa routing
        md.ndata = (bit<152>) (hdr.rec.routeid >> 8);
        md.diff = (bit<8>) hdr.rec.routeid;

        hdr.rec.ts = ig_intr_md.ingress_mac_tstamp[31:0];
        hdr.rec.num = 1;

        hdr.rec.sw_id = sw_id;

        ig_intr_tm_md.ucast_egress_port = port_user;
    }

    action send_next_1(bit<16> link_id) {
        hdr.rec.sw = link_id;
    }
    action send_next_2() {
        // PolKa routing
        md.nres = hash2.get(md.ndata);
        hdr.rec.sw = (bit<16>) (md.nres^md.diff); // Next link by PolKa
    }
    action send_next_3() {
        // PolKa routing
        md.nres = hash3.get(md.ndata);
        hdr.rec.sw = (bit<16>) (md.nres^md.diff); // Next link by PolKa
    }
    action send_next_4() {
        // PolKa routing
        md.nres = hash4.get(md.ndata);
        hdr.rec.sw = (bit<16>) (md.nres^md.diff); // Next link by PolKa
    }
    action send_next_5() {
        // PolKa routing
        md.nres = hash5.get(md.ndata);
        hdr.rec.sw = (bit<16>) (md.nres^md.diff); // Next link by PolKa
    }
    action send_next_6(bit<16> link_id) {
        hdr.rec.sw = link_id;
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
    action match(bit<16> link, bit<160> routeIdPacket) {
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

        hdr.rec.routeid = routeIdPacket;

        ig_intr_tm_md.ucast_egress_port = rec_port;
        ig_intr_tm_md.bypass_egress = 1w1;
    }

    action match_arp(bit<16> link, bit<160> routeIdPacket) {
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

        hdr.rec.routeid = routeIdPacket;

        ig_intr_tm_md.ucast_egress_port = rec_port;
        ig_intr_tm_md.bypass_egress = 1w1;
    }

    action match_arp_direct(PortId_t port) {
        ig_intr_tm_md.ucast_egress_port = port;
    }

    // Slice
    action slice_select_dst(bit<160> routeIdPacket){
        hdr.rec.routeid = routeIdPacket;
    }

    action slice_select_src(bit<160> routeIdPacket){
        hdr.rec.routeid = routeIdPacket;
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

    table basic_fwd_hash {
        key = {
            hdr.rec.sw_id : exact;
            hdr.rec.dest_ip   : exact;
        }
        actions = {
            send_next_1;
            send_next_2;
            send_next_3;
            send_next_4;
            send_next_5;
            send_next_6;
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

   table slice_dst {
       key = {
           hdr.udp.dst_port   : exact;
       }
       actions = {
           slice_select_dst;
           @defaultonly NoAction;
       }
       const default_action = NoAction();
       size = 128;
   }

   table slice_src {
       key = {
           hdr.udp.src_port   : exact;
       }
       actions = {
           slice_select_src;
           @defaultonly NoAction;
       }
       const default_action = NoAction();
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
            slice_dst.apply();
            slice_src.apply();
        }
        else if (hdr.vlan_tag.isValid() && !hdr.rec.isValid() && hdr.arp.isValid()) {
            arp_fwd.apply();
        } else {
            // If the recirculation header is valid, match the switch ID
            // Then verify the timestamp difference (latency)
            // Apply the packet_loss value with the random number generated
            // Verify if the switch is the final one or need to be processed by the next one
            if (hdr.rec.isValid()) {
                //Number of switch
                if (hdr.rec.sw == 0){                   // 0 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action0.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss0) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 1){                   // 1 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action1.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss1) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 2){                   // 2 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action2.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss2) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 3){                   // 3 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action3.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss3) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 4){                   // 4 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action4.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss4) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 5){                   // 5 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action5.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss5) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 6){                   // 6 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action6.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss6) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 7){                   // 7 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action7.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss7) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }
                else if (hdr.rec.sw == 8){                   // 8 - ID switch
                    bit<8> value_tscal;
                    md.ts_diff = 0;
                    comp_diff();
    		     //apply the jitter
		     if(hdr.rec.signal==0){
		         apply_more_jitter();
      		     }else{
   		         if(ax_action.execute(1)==1)
		     	     apply_less_jitter();
		     }
                    value_tscal = tscal_action8.execute(1);
                    if (value_tscal == 1){
                        bit<10> R = rnd.get();
                        if (R >= pkt_loss8) {            // @2-% of pkt loss 
                            basic_fwd.apply();
                            basic_fwd_hash.apply();
                        }else{
                            drop();
                        } 
                    }else {
                        recirculate(rec_port);          // Recirculation port (e.g., loopback interface)
                    }   
                }else{
                    drop();
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
