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

import os

def gen_multiple_old(p4_code, routing_model, tofino_version, pipeline_0, pipeline_1, pipeline_2, pipeline_3): 
    f = open("./p4src/multiprogram_custom_bfrt.conf", "w")

    p4_original = p4_code[0][1] # file name of original user p4 code


    p4_name = p4_original.split(".")
    if p4_name[0].find('/') != -1:
        p4_copy = p4_name[0].split("/")
        p4_copy = p4_copy[-1] + "_mod"
    else:
    	p4_copy = p4_name[0] + "_mod"	
    
    if (routing_model == 0 or routing_model == 2):
        p7_p4code = "p7_default"
    if (routing_model == 1):
        p7_p4code = "p7_polka"

    if (tofino_version == 1):
        f.write("{\n")
        f.write("    \"chip_list\": [\n")
        f.write("        {\n")
        f.write("            \"id\": \"asic-0\",\n")
        f.write("            \"chip_family\": \"Tofino\",\n")
        f.write("            \"instance\": 0,\n")
        f.write("            \"pcie_sysfs_prefix\": \"/sys/devices/pci0000:00/0000:00:03.0/0000:05:00.0\",\n")
        f.write("            \"pcie_domain\": 0,\n")
        f.write("            \"pcie_bus\": 5,\n")
        f.write("            \"pcie_fn\": 0,\n")
        f.write("            \"pcie_dev\": 0,\n")
        f.write("            \"pcie_int_mode\": 1,\n")
        f.write("            \"sds_fw_path\": \"share/tofino_sds_fw/avago/firmware\"\n")
        f.write("        }\n")
        f.write("    ],\n")
        f.write("    \"instance\": 0,\n")
        f.write("    \"p4_devices\": [\n")
        f.write("        {\n")
        f.write("            \"device-id\": 0,\n")
        f.write("            \"p4_programs\": [\n")
        f.write("                {\n")
        f.write("                    \"program-name\": \"" + str(p7_p4code) + "\",\n")
        f.write("                    \"bfrt-config\": \"share/tofinopd/" + str(p7_p4code) + "/bf-rt.json\",\n")
        f.write("                    \"p4_pipelines\": [\n")
        f.write("                        {\n")
        f.write("                            \"p4_pipeline_name\": \"pipe_p7\",\n")
        f.write("                            \"context\": \"share/tofinopd/" + str(p7_p4code) + "/pipe_p7/context.json\",\n")
        f.write("                            \"config\": \"share/tofinopd/" + str(p7_p4code) + "/pipe_p7/tofino.bin\",\n")
        f.write("                            \"pipe_scope\": [1]\n")
        f.write("                        }\n")
        f.write("                    ]\n")
        f.write("                },\n")
        f.write("                {\n")
        f.write("                    \"program-name\": \"" + p4_copy + "\",\n")
        f.write("                    \"bfrt-config\": \"share/tofinopd/" + p4_copy + "/bf-rt.json\",\n")
        f.write("                    \"p4_pipelines\": [\n")
        f.write("                        {\n")
        f.write("                            \"p4_pipeline_name\": \"pipe\",\n")
        f.write("                            \"context\": \"share/tofinopd/" + p4_copy + "/pipe/context.json\",\n")
        f.write("                            \"config\": \"share/tofinopd/" + p4_copy + "/pipe/tofino.bin\",\n")
        f.write("                            \"pipe_scope\": [0]\n")
        f.write("                        }\n")
        f.write("                    ]\n")
        f.write("                }\n")
        f.write("            ],\n")
        f.write("            \"agent0\": \"lib/libpltfm_mgr.so\"\n")
        f.write("        }\n")
        f.write("    ]\n")
        f.write("}\n")


    if tofino_version == 2:
        f.write("{\n")
        f.write("    \"chip_list\": [\n")
        f.write("        {\n")
        f.write("            \"chip_family\": \"Tofino2\",\n")
        f.write("            \"instance\": 0,\n")
        f.write("            \"pcie_sysfs_prefix\": \"/sys/devices/pci0000:00/0000:00:03.0/0000:05:00.0\",\n")
        f.write("            \"pcie_int_mode\": 1,\n")
        f.write("            \"sds_fw_path\": \"share/tofino_sds_fw/avago/firmware\",\n")
        f.write("            \"microp_fw_path\": \"share/microp_fw/microp/tof2/fw/\"\n")
        f.write("        }\n")
        f.write("    ],\n")
        f.write("    \"p4_devices\": [\n")
        f.write("        {\n")
        f.write("            \"device-id\": 0,\n")
        f.write("            \"p4_programs\": [\n")
        f.write("                {\n")
        f.write("                    \"program-name\": \"" + str(p7_p4code) + "\",\n")
        f.write("                    \"bfrt-config\": \"share/tofino2pd/" + str(p7_p4code) + "/bf-rt.json\",\n")
        f.write("                    \"p4_pipelines\": [\n")
        f.write("                        {\n")
        f.write("                            \"p4_pipeline_name\": \"pipe_p7\",\n")
        f.write("                            \"context\": \"share/tofino2pd/" + str(p7_p4code) + "/pipe_p7/context.json\",\n")
        f.write("                            \"config\": \"share/tofino2pd/" + str(p7_p4code) + "/pipe_p7/tofino2.bin\",\n")
        f.write("                            \"pipe_scope\": [0, 1]\n")
        f.write("                        }\n")
        f.write("                    ]\n")
        f.write("                },\n")
        f.write("                {\n")
        f.write("                    \"program-name\": \"" + p4_copy + "\",\n")
        f.write("                    \"bfrt-config\": \"share/tofino2pd/" + p4_copy + "/bf-rt.json\",\n")
        f.write("                    \"p4_pipelines\": [\n")
        f.write("                        {\n")
        f.write("                            \"p4_pipeline_name\": \"pipe\",\n")
        f.write("                            \"context\": \"share/tofino2pd/" + p4_copy + "/pipe/context.json\",\n")
        f.write("                            \"config\": \"share/tofino2pd/" + p4_copy + "/pipe/tofino2.bin\",\n")
        f.write("                            \"pipe_scope\": [2, 3]\n")
        f.write("                        }\n")
        f.write("                    ]\n")
        f.write("                }\n")
        f.write("            ],\n")
        f.write("            \"agent0\": \"lib/libpltfm_mgr.so\"\n")
        f.write("        }\n")
        f.write("    ]\n")
        f.write("}\n")



def gen_multiple(p4_code, routing_model, tofino_version, pipeline_0, pipeline_1, pipeline_2, pipeline_3):
    """
    Versão estrita (sem fallbacks).
    - Assume que cada pipeline não-None é ou 'spine' (case-insensitive) ou um id presente em p4_code[*][0].
    - Agrupa pipelines que apontem para o mesmo programa (p7 ou mesmo p4_copy) em um único bloco com "pipe_scope": [..].
    - Mantém formato textual exato (f.write linha a linha) do arquivo original.
    """
    out_path = "./p4src/multiprogram_custom_bfrt.conf"
    f = open(out_path, "w")

    # determina p7 (p7_default ou p7_polka)
    if (routing_model == 0 or routing_model == 2):
        p7_p4code = "p7_default"
    elif (routing_model == 1):
        p7_p4code = "p7_polka"
    else:
        p7_p4code = "p7_default"

    # mapeamento id -> nome_original (string keys) — assumimos que p4_code está correto
    id_to_name = {}
    for entry in p4_code:
        if len(entry) >= 2:
            id_to_name[str(entry[0])] = entry[1]

    # função para gerar nome _mod
    def make_p4_copy_name(orig_name):
        base = os.path.basename(orig_name)
        base_noext = os.path.splitext(base)[0]
        return base_noext + "_mod"

    # lista de pipeline vars
    pipeline_vars = {
        0: pipeline_0,
        1: pipeline_1,
        2: pipeline_2,
        3: pipeline_3
    }

    # Agrupa: chave -> {type: 'p7'|'p4', orig: nome_original, indices: [..]}
    groups = {}

    for idx in range(4):
        pv = pipeline_vars.get(idx, None)
        if pv is None:
            # pula pipelines não-definidos
            continue

        # detecta 'spine' (case-insensitive) -> vai para p7
        if isinstance(pv, str) and pv.lower() == "spine":
            key = p7_p4code
            groups.setdefault(key, {"type": "p7", "orig": p7_p4code, "indices": []})["indices"].append(idx)
            continue

        # caso normal: pv deve corresponder a uma chave em p4_code (comparando como string)
        pv_str = str(pv)
        if pv_str not in id_to_name:
            raise ValueError(f"Pipeline {idx} refere '{pv_str}' que não existe em p4_code. \
Garanta que p4_code contenha uma entrada com [0] == '{pv_str}'.")
        matched = id_to_name[pv_str]  # nome do arquivo P4 original
        p4_copy = make_p4_copy_name(matched)
        groups.setdefault(p4_copy, {"type": "p4", "orig": matched, "indices": []})["indices"].append(idx)

    # --- escreve arquivo no formato textual exato (f.write linha a linha) ---

    if (tofino_version == 1):
        # bloco Tofino1
        f.write("{\n")
        f.write("    \"chip_list\": [\n")
        f.write("        {\n")
        f.write("            \"id\": \"asic-0\",\n")
        f.write("            \"chip_family\": \"Tofino\",\n")
        f.write("            \"instance\": 0,\n")
        f.write("            \"pcie_sysfs_prefix\": \"/sys/devices/pci0000:00/0000:00:03.0/0000:05:00.0\",\n")
        f.write("            \"pcie_domain\": 0,\n")
        f.write("            \"pcie_bus\": 5,\n")
        f.write("            \"pcie_fn\": 0,\n")
        f.write("            \"pcie_dev\": 0,\n")
        f.write("            \"pcie_int_mode\": 1,\n")
        f.write("            \"sds_fw_path\": \"share/tofino_sds_fw/avago/firmware\"\n")
        f.write("        }\n")
        f.write("    ],\n")
        f.write("    \"instance\": 0,\n")
        f.write("    \"p4_devices\": [\n")
        f.write("        {\n")
        f.write("            \"device-id\": 0,\n")
        f.write("            \"p4_programs\": [\n")

        # Escrever p7 primeiro (se existir)
        wrote_any = False
        if p7_p4code in groups:
            info = groups[p7_p4code]
            indices = sorted(info["indices"])
            f.write("                {\n")
            f.write("                    \"program-name\": \"" + str(p7_p4code) + "\",\n")
            f.write("                    \"bfrt-config\": \"share/tofinopd/" + str(p7_p4code) + "/bf-rt.json\",\n")
            f.write("                    \"p4_pipelines\": [\n")
            f.write("                        {\n")
            f.write("                            \"p4_pipeline_name\": \"pipe_p7\",\n")
            f.write("                            \"context\": \"share/tofinopd/" + str(p7_p4code) + "/pipe_p7/context.json\",\n")
            f.write("                            \"config\": \"share/tofinopd/" + str(p7_p4code) + "/pipe_p7/tofino.bin\",\n")
            f.write("                            \"pipe_scope\": [" + ", ".join(str(i) for i in indices) + "]\n")
            f.write("                        }\n")
            f.write("                    ]\n")
            f.write("                }")
            wrote_any = True

        # Escrever demais grupos p4 (ordenados para determinismo)
        p4_keys = sorted([k for k in groups.keys() if groups[k]["type"] == "p4"])
        if p4_keys:
            if wrote_any:
                f.write(",\n")
            for pi, key in enumerate(p4_keys):
                info = groups[key]
                indices = sorted(info["indices"])
                f.write("                {\n")
                f.write("                    \"program-name\": \"" + key + "\",\n")
                f.write("                    \"bfrt-config\": \"share/tofinopd/" + key + "/bf-rt.json\",\n")
                f.write("                    \"p4_pipelines\": [\n")
                f.write("                        {\n")
                f.write("                            \"p4_pipeline_name\": \"pipe\",\n")
                f.write("                            \"context\": \"share/tofinopd/" + key + "/pipe/context.json\",\n")
                f.write("                            \"config\": \"share/tofinopd/" + key + "/pipe/tofino.bin\",\n")
                f.write("                            \"pipe_scope\": [" + ", ".join(str(i) for i in indices) + "]\n")
                f.write("                        }\n")
                f.write("                    ]\n")
                if pi == len(p4_keys) - 1:
                    f.write("                }\n")
                else:
                    f.write("                },\n")

        # Fecha blocos finais do Tofino1
        f.write("            ],\n")
        f.write("            \"agent0\": \"lib/libpltfm_mgr.so\"\n")
        f.write("        }\n")
        f.write("    ]\n")
        f.write("}\n")

    else:
        # Tofino2 — comportamento idêntico, agrupando por programa. (Só escrevemos grupos para pipelines fornecidos.)
        f.write("{\n")
        f.write("    \"chip_list\": [\n")
        f.write("        {\n")
        f.write("            \"chip_family\": \"Tofino2\",\n")
        f.write("            \"instance\": 0,\n")
        f.write("            \"pcie_sysfs_prefix\": \"/sys/devices/pci0000:00/0000:00:03.0/0000:05:00.0\",\n")
        f.write("            \"pcie_int_mode\": 1,\n")
        f.write("            \"sds_fw_path\": \"share/tofino_sds_fw/avago/firmware\",\n")
        f.write("            \"microp_fw_path\": \"share/microp_fw/microp/tof2/fw/\"\n")
        f.write("        }\n")
        f.write("    ],\n")
        f.write("    \"p4_devices\": [\n")
        f.write("        {\n")
        f.write("            \"device-id\": 0,\n")
        f.write("            \"p4_programs\": [\n")

        wrote_any = False
        if p7_p4code in groups:
            info = groups[p7_p4code]
            indices = sorted(info["indices"])
            f.write("                {\n")
            f.write("                    \"program-name\": \"" + str(p7_p4code) + "\",\n")
            f.write("                    \"bfrt-config\": \"share/tofino2pd/" + str(p7_p4code) + "/bf-rt.json\",\n")
            f.write("                    \"p4_pipelines\": [\n")
            f.write("                        {\n")
            f.write("                            \"p4_pipeline_name\": \"pipe_p7\",\n")
            f.write("                            \"context\": \"share/tofino2pd/" + str(p7_p4code) + "/pipe_p7/context.json\",\n")
            f.write("                            \"config\": \"share/tofino2pd/" + str(p7_p4code) + "/pipe_p7/tofino2.bin\",\n")
            f.write("                            \"pipe_scope\": [" + ", ".join(str(i) for i in indices) + "]\n")
            f.write("                        }\n")
            f.write("                    ]\n")
            f.write("                }")
            wrote_any = True

        p4_keys = sorted([k for k in groups.keys() if groups[k]["type"] == "p4"])
        if p4_keys:
            if wrote_any:
                f.write(",\n")
            for pi, key in enumerate(p4_keys):
                info = groups[key]
                indices = sorted(info["indices"])
                f.write("                {\n")
                f.write("                    \"program-name\": \"" + key + "\",\n")
                f.write("                    \"bfrt-config\": \"share/tofino2pd/" + key + "/bf-rt.json\",\n")
                f.write("                    \"p4_pipelines\": [\n")
                f.write("                        {\n")
                f.write("                            \"p4_pipeline_name\": \"pipe\",\n")
                f.write("                            \"context\": \"share/tofino2pd/" + key + "/pipe/context.json\",\n")
                f.write("                            \"config\": \"share/tofino2pd/" + key + "/pipe/tofino2.bin\",\n")
                f.write("                            \"pipe_scope\": [" + ", ".join(str(i) for i in indices) + "]\n")
                f.write("                        }\n")
                f.write("                    ]\n")
                if pi == len(p4_keys) - 1:
                    f.write("                }\n")
                else:
                    f.write("                },\n")

        # Fecha blocos finais do Tofino2
        f.write("            ],\n")
        f.write("            \"agent0\": \"lib/libpltfm_mgr.so\"\n")
        f.write("        }\n")
        f.write("    ]\n")
        f.write("}\n")

    f.close()

    
