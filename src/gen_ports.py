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


def alocar_porta_v2(ports_dict, usados, usado_por_prefixo, bw):
    """
    Aloca uma porta/canal respeitando:
      - > 50 Gbps: precisa dos 4 canais (0,1,2,3) da MESMA porta livres.
      - 25 < bw <= 50 Gbps: precisa de um PAR {0,1} OU {2,3} da MESMA porta livres.
      - bw <= 25 Gbps: qualquer canal livre.
    Suporta portas com número variável de canais (derivado de ports_dict).
    Mantém compatibilidade com 'usados' e 'usado_por_prefixo':
      - 'usados' recebe apenas a chave retornada (canônica) da alocação;
      - 'usado_por_prefixo[prefixo]' recebe TODOS os canais bloqueados pela regra.
    """

    # Pré-processa canais existentes e disponíveis por prefixo,
    # considerando 'usados' e reservas em 'usado_por_prefixo'.
    canais_existentes_por_prefixo = {}
    for chave in ports_dict.keys():
        prefixo, canal = chave.split("/")
        canais_existentes_por_prefixo.setdefault(prefixo, set()).add(canal)

    def canais_disponiveis(prefixo):
        bloqueados = usado_por_prefixo.get(prefixo, set())
        disp = set()
        for canal in canais_existentes_por_prefixo.get(prefixo, set()):
            chave = f"{prefixo}/{canal}"
            if chave in usados:
                continue
            if canal in bloqueados:
                continue
            disp.add(canal)
        return disp

    # Regra 1: > 50 Gbps — requer {0,1,2,3} livres e existentes
    if bw > 50_000_000_000:
        required = {"0", "1", "2", "3"}
        for prefixo, existentes in canais_existentes_por_prefixo.items():
            # porta precisa TER os 4 canais
            if not required.issubset(existentes):
                continue
            disp = canais_disponiveis(prefixo)
            if required.issubset(disp):
                # Aloca de forma canônica retornando prefixo/0 e bloqueia os 4
                chave = f"{prefixo}/0"
                usados.add(chave)
                usado_por_prefixo[prefixo] = set(usado_por_prefixo.get(prefixo, set())) | required
                return chave
        return None

    # Regra 2: 25 < bw <= 50 Gbps — requer par {0,1} OU {2,3} livres e existentes
    if bw > 25_000_000_000:
        pares = [({"0", "1"}, "0"), ({"2", "3"}, "2")]  # (conjunto_do_par, canal_de_retorno)
        for prefixo, existentes in canais_existentes_por_prefixo.items():
            disp = canais_disponiveis(prefixo)
            # Se já há bloqueios, eles são respeitados por 'canais_disponiveis'
            for par, canal_retorno in pares:
                if par.issubset(existentes) and par.issubset(disp):
                    # bloquear AMBOS canais do par
                    chave = f"{prefixo}/{canal_retorno}"
                    usados.add(chave)
                    usado_por_prefixo.setdefault(prefixo, set()).update(par)
                    return chave
        return None

    # Regra 3: <= 25 Gbps — qualquer canal livre (inclusive portas de 1 canal)
    for prefixo in canais_existentes_por_prefixo.keys():
        disp = sorted(canais_disponiveis(prefixo), key=lambda x: int(x) if x.isdigit() else x)
        if disp:
            canal = disp[0]
            chave = f"{prefixo}/{canal}"
            usados.add(chave)
            usado_por_prefixo.setdefault(prefixo, set()).add(canal)
            return chave

    return None





def generate_port(hosts, links, vlans, rec_bw, ports_pipe0, ports_pipe1, ports_pipe2, ports_pipe3, pipeline_0, pipeline_1, pipeline_2, pipeline_3, sw_p4):
	

    #trying final updates

    #dictionaries with available ports for each pipeline/functionality, maybe not all are used
    usados_pipe_emulation = set()
    usados_pipe_user0 = set()
    usados_pipe_user1 = set()
    usados_pipe_user2 = set()

    usado_por_prefixo_pipe_emulation = {}
    usado_por_prefixo_pipe_user0 = {}
    usado_por_prefixo_pipe_user1 = {}
    usado_por_prefixo_pipe_user2 = {}

    ports_emulation_pipeline = {}
    ports_user0_pipeline = {}
    ports_user1_pipeline = {}
    ports_user2_pipeline = {}

    # dicionário para mapear cada user_code -> qual user ele ocupa
    user_map = {}

    # lista só para iterar de forma organizada
    pipes = [
        (pipeline_0, ports_pipe0),
        (pipeline_1, ports_pipe1),
        (pipeline_2, ports_pipe2),
        (pipeline_3, ports_pipe3),
    ]

    # filling the dictionaries with available ports for each p4 code. 
    # if the same p4 code is used in more than one pipe, the ports are added to the same dictionary
    for pipe_name, ports in pipes:
        if pipe_name in ("spine", None, "trafficGen"):
            continue  # ignora

        if pipe_name not in user_map:
            # atribui o próximo user disponível
            user_map[pipe_name] = len(user_map)

        user_idx = user_map[pipe_name]

        if user_idx == 0:
            ports_user0_pipeline.update(ports)
        elif user_idx == 1:
            ports_user1_pipeline.update(ports)
        elif user_idx == 2:
            ports_user2_pipeline.update(ports)


    #filling the ports for the emulation pipelines
    if pipeline_0 == "spine":
        ports_emulation_pipeline.update(ports_pipe0)

    if pipeline_1 == "spine":
        ports_emulation_pipeline.update(ports_pipe1)

    if pipeline_2 == "spine":
        ports_emulation_pipeline.update(ports_pipe2)

    if pipeline_3 == "spine":
        ports_emulation_pipeline.update(ports_pipe3)

    #testing
    #ToDo Finalize
    # Conjunto para marcar portas ocupadas em cada pipe
    usados_pipe0 = set()
    usados_pipe1 = set()
    # Para controlar prefixos e quantas portas foram usadas deles
    usado_por_prefixo_pipe0 = {}
    usado_por_prefixo_pipe1 = {}

    # lista de saída
    links_port_map = []


    print("Port mapping new version")
	#Creating the pairs of loopback ports for each link
    links_port_map = []
    for i in range(len(links)):

        #trying to find a port on the emulation pipeline
        chave0 = alocar_porta_v2(ports_emulation_pipeline, usados_pipe_emulation, usado_por_prefixo_pipe_emulation, links[i][2])

        if chave0 is None:
                print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                exit()


        #trying to find a port on the user pipeline

        p4_a = sw_p4.get(links[i][0])
        p4_b = sw_p4.get(links[i][1])

        # Caso (1) → os dois existem e são diferentes, so it will generate two different mappings
        if p4_a is not None and p4_b is not None and p4_a != p4_b:
            #ToDo: check if it is right
            # pega o índice de usuário para cada P4
            user_idx_a = user_map[p4_a]
            user_idx_b = user_map[p4_b]

            # aloca chave1 para o primeiro switch
            if user_idx_a == 0:
                chave1 = alocar_porta_v2(ports_user0_pipeline, usados_pipe_user0, usado_por_prefixo_pipe_user0, links[i][2])
                if chave1 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry1 = [links[i][0], links[i][1], links[i][2], chave1, ports_user0_pipeline[chave1], chave0, ports_emulation_pipeline[chave0]]
            elif user_idx_a == 1:
                chave1 = alocar_porta_v2(ports_user1_pipeline, usados_pipe_user1, usado_por_prefixo_pipe_user1, links[i][2])
                if chave1 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry1 = [links[i][0], links[i][1], links[i][2], chave1, ports_user1_pipeline[chave1], chave0, ports_emulation_pipeline[chave0]]
            elif user_idx_a == 2:
                chave1 = alocar_porta_v2(ports_user2_pipeline, usados_pipe_user2, usado_por_prefixo_pipe_user2, links[i][2])
                if chave1 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry1 = [links[i][0], links[i][1], links[i][2], chave1, ports_user2_pipeline[chave1], chave0, ports_emulation_pipeline[chave0]]

            links_port_map.append(port_map_entry1)

            # aloca chave2 para o segundo switch
            if user_idx_b == 0:
                chave2 = alocar_porta_v2(ports_user0_pipeline, usados_pipe_user0, usado_por_prefixo_pipe_user0, links[i][2])
                if chave2 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry2 = [links[i][0], links[i][1], links[i][2], chave2, ports_user0_pipeline[chave2], chave0, ports_emulation_pipeline[chave0]]
            elif user_idx_b == 1:
                chave2 = alocar_porta_v2(ports_user1_pipeline, usados_pipe_user1, usado_por_prefixo_pipe_user1, links[i][2])
                if chave2 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry2 = [links[i][0], links[i][1], links[i][2], chave2, ports_user1_pipeline[chave2], chave0, ports_emulation_pipeline[chave0]]
            elif user_idx_b == 2:
                chave2 = alocar_porta_v2(ports_user2_pipeline, usados_pipe_user2, usado_por_prefixo_pipe_user2, links[i][2])
                if chave2 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry2 = [links[i][0], links[i][1], links[i][2], chave2, ports_user2_pipeline[chave2], chave0, ports_emulation_pipeline[chave0]]

            links_port_map.append(port_map_entry2)





        # Case (2) → one is host or both are the same P4 code, so it will use the same mapping for both    
        else:
            #get the name of the p4 code used
            p4_nome = p4_a or p4_b

            user_idx = user_map[p4_nome]

            if user_idx == 0:
                chave1 = alocar_porta_v2(ports_user0_pipeline, usados_pipe_user0, usado_por_prefixo_pipe_user0, links[i][2])
                if chave1 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry = [links[i][0], links[i][1], links[i][2], chave1, ports_user0_pipeline[chave1], chave0, ports_emulation_pipeline[chave0]]
            elif user_idx == 1:
                chave1 = alocar_porta_v2(ports_user1_pipeline, usados_pipe_user1, usado_por_prefixo_pipe_user1, links[i][2])
                if chave1 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry = [links[i][0], links[i][1], links[i][2], chave1, ports_user1_pipeline[chave1], chave0, ports_emulation_pipeline[chave0]]
            elif user_idx == 2:
                chave1 = alocar_porta_v2(ports_user2_pipeline, usados_pipe_user2, usado_por_prefixo_pipe_user2, links[i][2])
                if chave1 is None:
                    print(f"⚠️ Não foi possível mapear link {links[i][0]}-{links[i][1]} com bw {links[i][2]}")
                    exit()
                port_map_entry = [links[i][0], links[i][1], links[i][2], chave1, ports_user2_pipeline[chave1], chave0, ports_emulation_pipeline[chave0]]


            #port_map_entry = [links[i][0], links[i][1], links[i][2], chave0, ports_pipe0[chave0], chave1, ports_pipe1[chave1]]
	
            links_port_map.append(port_map_entry)

        

        #chave1 = alocar_porta_v2(ports_pipe1, usados_pipe1, usado_por_prefixo_pipe1, links[i][2])


        

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