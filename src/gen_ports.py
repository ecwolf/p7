 ################################################################################
 # Copyright 2024 INTRIG
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

import re

# função auxiliar para tentar alocar uma porta em um pipe
def alocar_porta(ports_dict, usados, usado_por_prefixo, bw):
    # tentamos percorrer por prefixo
    for chave in ports_dict.keys():
        if chave in usados:
            continue
        prefixo = chave.split("/")[0]
        # quantas já usei deste prefixo?
        usadas_no_prefixo = usado_por_prefixo.get(prefixo, set())

        # regra 1: bw > 50 Gbps → só pode usar x/0 e exclusividade
        if bw > 50_000_000_000:
            if usadas_no_prefixo:  # já usei alguma desse prefixo
                continue
            if chave.endswith("/0"):
                # aloca
                usados.add(chave)
                usado_por_prefixo[prefixo] = {"0","1","2","3"}  # bloqueia todas
                return chave

        # regra 2: 25 < bw <= 50 Gbps → pode usar x/0 e x/2 no mesmo prefixo
        elif bw > 25_000_000_000:
            # se já usei alguma do prefixo, tem que respeitar a combinação
            if usadas_no_prefixo and not (usadas_no_prefixo <= {"0","2"}):
                # já tinha usado uma porta que não é 0 ou 2 nesse prefixo
                continue
            # posso usar x/0 ou x/2, se ainda não usados nesse prefixo
            if chave.endswith("/0") and "0" not in usadas_no_prefixo:
                usados.add(chave)
                usado_por_prefixo.setdefault(prefixo, set()).add("0")
                return chave
            if chave.endswith("/2") and "2" not in usadas_no_prefixo:
                usados.add(chave)
                usado_por_prefixo.setdefault(prefixo, set()).add("2")
                return chave

        # regra 3: bw <= 25 Gbps → posso usar x/0,x/1,x/2,x/3 livremente
        else:
            if chave.split("/")[1] not in usadas_no_prefixo:
                usados.add(chave)
                usado_por_prefixo.setdefault(prefixo, set()).add(chave.split("/")[1])
                return chave

    # se não conseguiu alocar
    return None






def generate_port(hosts, links, vlans, rec_bw, ports_pipe0, ports_pipe1):
	

	#testing

	# Conjunto para marcar portas ocupadas em cada pipe
	usados_pipe0 = set()
	usados_pipe1 = set()
    # Para controlar prefixos e quantas portas foram usadas deles
	usado_por_prefixo_pipe0 = {}
	usado_por_prefixo_pipe1 = {}

    # lista de saída
	links_port_map = []



	#Creating the pairs of loopback ports for each link
	links_port_map = []
	for i in range(len(links)):
		chave0 = alocar_porta(ports_pipe0, usados_pipe0, usado_por_prefixo_pipe0, links[i][2])
		chave1 = alocar_porta(ports_pipe1, usados_pipe1, usado_por_prefixo_pipe1, links[i][2])

		if chave0 is None or chave1 is None:
			print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
			exit()


		port_map_entry = [links[i][0], links[i][1], links[i][2], chave0, ports_pipe0[chave0], chave1, ports_pipe1[chave1]]
	
		links_port_map.append(port_map_entry)

	print(links_port_map)

	f = open("./files/ports_config.txt", "w")

	#Acces ucli/pm
	f.write("ucli\n")
	f.write("pm\n")

	#Ports host configuration
	for i in range(len(hosts)):
		if hosts[i][5] == "False":
			feec = "NONE"
		f.write("port-add " + str(hosts[i][1]) + " " + str(int(hosts[i][3]/1000000000)) + "G" + " " + str(feec) + "\n")
		f.write("port-enb " + str(hosts[i][1]) + "\n")
		if hosts[i][4] == "False":
			f.write("an-set " + str(hosts[i][1]) + " 2" + "\n")
			f.write("port-dis " + str(hosts[i][1]) + "\n")
			f.write("port-enb " + str(hosts[i][1]) + "\n")

	#Ports link configuration
	for i in range(len(links_port_map)):
		if links_port_map[i][2] > 50000000000:
			f.write("port-add " + str(links_port_map[i][3]) + " 100G" + " NONE\n")
			f.write("port-loopback " + str(links_port_map[i][3]) + " mac-near\n")
			f.write("port-enb " + str(links_port_map[i][3]) + "\n")
			f.write("port-add " + str(links_port_map[i][5]) + " 100G" + " NONE\n")
			f.write("port-loopback " + str(links_port_map[i][5]) + " mac-near\n")
			f.write("port-enb " + str(links_port_map[i][5]) + "\n")
		elif links_port_map[i][2] > 25000000000:
			f.write("port-add " + str(links_port_map[i][3]) + " 50G" + " NONE\n")
			f.write("port-loopback " + str(links_port_map[i][3]) + " mac-near\n")
			f.write("port-enb " + str(links_port_map[i][3]) + "\n")
			f.write("port-add " + str(links_port_map[i][5]) + " 50G" + " NONE\n")
			f.write("port-loopback " + str(links_port_map[i][5]) + " mac-near\n")
			f.write("port-enb " + str(links_port_map[i][5]) + "\n")
		else:
			f.write("port-add " + str(links_port_map[i][3]) + " 25G" + " NONE\n")
			f.write("port-loopback " + str(links_port_map[i][3]) + " mac-near\n")
			f.write("port-enb " + str(links_port_map[i][3]) + "\n")
			f.write("port-add " + str(links_port_map[i][5]) + " 25G" + " NONE\n")
			f.write("port-loopback " + str(links_port_map[i][5]) + " mac-near\n")
			f.write("port-enb " + str(links_port_map[i][5]) + "\n")

	f.write("show" + "\n")


	

	f.close()

	return links_port_map