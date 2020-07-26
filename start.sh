#!/usr/bin/env bash

###################################################################################
# Author: Callum Tyler 2020
#
### Description
# Launch data generation, flow estimation & results plot for Open Channel Simulation
# 
###################################################################################

python3 data_gen.py
./flow
python3 data_plot.py ocf_meas.csv ocf_prev.csv ocf_curr.csv ocf_data.csv