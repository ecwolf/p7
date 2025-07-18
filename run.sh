#!/bin/bash

if [ "$COMPILE_P4" == "0" ] && [ "$RUN_SWITCH" == "0" ]; then
    echo "P7 compiled and supporting files generated"
    exit 1
fi

# Check if SDE is defined
if [ -z "$SDE" ]; then
    echo "SDE is not defined!"
    echo "Need to define the SDE environmental variable"
    echo "to Compile the P4 codes or Run the switch"
    exit 1
else
    echo "Using SDE path: $SDE"
fi

# Check if Tools is defined
if [ "$NO_TOOLS" == "1" ] || [ "$COMPILE_P4" == "0" ]; then
    echo "Not using SDE_tools"
else
    if [ -z "$SDE_tools" ]; then
        echo "SDE_tools is not defined!"
        echo "Define the SDE_tools path or manually compile the P4 Codes"
        echo "Using SDE_tools:"
        echo "  export SDE_tools=<tools path>"
        echo "Manually compilling:"
        echo "  Run the main.py script with --no-tools flag"
        echo "  Example:"
        echo "      python main.py --no-tools"
        exit 1
    else
        echo "Using SDE_tools path: $SDE_tools"
    fi
fi

p7_dir=$(pwd)
echo "Using P7 directory: $p7_dir"

if [ "$COMPILE_P4" == "1" ]; then
    echo "**********************************************************"
    echo "**********          Compiling P7 P4 code        **********" 
    echo "**********************************************************"
    if [ "$POLKA" == "1" ]; then
        $SDE_tools/p4_build.sh p4src/p7_polka.p4  
    else
        $SDE_tools/p4_build.sh p4src/p7_default.p4  
    fi
    echo "Compiling modified User P4 code $USERP4.p4"
    echo "**********************************************************"
    echo "*  Compiling modified User P4 code $USERP4.p4   *" 
    echo "**********************************************************"
    $SDE_tools/p4_build.sh p4src/$USERP4.p4  
fi

if [ "$RUN_SWITCH" == "0" ]; then
    echo "P4 files compiled"
    exit 1
fi

if [ "$COMPILE_P4" == "0" ]; then
    echo "WARNING You need to manully compile the P4 codes"
fi

echo "Killing old process"

killall bf_switchd
killall run_switchd

if [ -z "$SDE_INSTALL" ]; then
    echo "Loading drivers"
    bf_kdrv_mod_load $SDE_INSTALL
fi

echo "**********************************************************"
echo "**********           Starting the Switch        **********" 
echo "**********************************************************"

if [ "$POLKA" == "1" ]; then
    $SDE/run_switchd.sh -p p7_polka $USERP4 -c $p7_dir/p4src/multiprogram_custom_bfrt.conf &
else
    $SDE/run_switchd.sh -p p7_default $USERP4 -c $p7_dir/p4src/multiprogram_custom_bfrt.conf &
fi

sleep 45

echo "**********************************************************"
echo "**********      Loading table information       **********" 
echo "**********************************************************"
bfshell -b files/bfrt.py

echo "**********************************************************"
echo "**********           Configuring Ports          **********" 
echo "**********************************************************"
bfshell -f files/ports_config.txt -i
