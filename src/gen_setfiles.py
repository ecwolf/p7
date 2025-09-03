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
from pathlib import Path


def gen_set_files(p4_code, routing_model): 
    with open("./set_files.sh", "w") as f:
        f.write("################################################################################\n")
        f.write("# Copyright 2024 INTRIG\n")
        f.write("#\n")
        f.write("# Licensed under the Apache License, Version 2.0 (the \"License\");\n")
        f.write("# you may not use this file except in compliance with the License.\n")
        f.write("# You may obtain a copy of the License at\n")
        f.write("#\n")
        f.write("#     http://www.apache.org/licenses/LICENSE-2.0\n")
        f.write("#\n")
        f.write("# Unless required by applicable law or agreed to in writing, software\n")
        f.write("# distributed under the License is distributed on an \"AS IS\" BASIS,\n")
        f.write("# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n")
        f.write("# See the License for the specific language governing permissions and\n")
        f.write("# limitations under the License.\n")
        f.write("################################################################################\n")
        f.write("\n")
        f.write("#!/bin/bash\n")
        f.write("\n")
        f.write("cp files/p4rt.py p4src/p4rt/\n")
        if routing_model == 0 or routing_model == 2:
            f.write("cp files/p7_default.p4 p4src/\n")
        if routing_model == 1:
            f.write("cp files/p7_polka.p4 p4src/\n")

        # agora percorremos todos os códigos P4 da lista
        for name, p4file in p4_code:
            # Path.stem pega nome do arquivo sem extensão nem caminho
            stem = Path(p4file).stem
            p4_copy = f"{stem}_mod.p4"
            f.write(f"cp files/{p4_copy} p4src/\n")
