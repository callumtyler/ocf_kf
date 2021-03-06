###################################################################################
# Author: Callum Tyler 2020
#
### Description
# Plots esimates open channel flow. 
#
### Instructions:
# `python3 data_plot.py`
#
###################################################################################

import csv
import random
import math
import argparse
import os
import matplotlib.pyplot as plt
from numpy import genfromtxt
import numpy as np

class Data:
    def __init__(self):
        ## Initialise data
        self.data_flow_meas = []
        self.data_flow_curr = []
        self.data_flow_prev = []
        self.data_sim = []

    def load_data(self):
        ## Get current full path
        current_directory = os.getcwd()
        ## Load curr, meas, prev, sim data
        self.data_flow_curr = genfromtxt(current_directory + '/data/ocf_flow_curr.csv', delimiter=',')
        self.data_flow_prev = genfromtxt(current_directory + '/data/ocf_flow_prev.csv', delimiter=',')
        self.data_flow_meas = genfromtxt(current_directory + '/data/ocf_flow_meas.csv', delimiter=',')
        self.data_sim = genfromtxt(current_directory + '/' + '/data/ocf_data.csv', delimiter=',')

    def plot(self):
        ## Prepare time data for plot   
        data_time = np.empty([len(self.data_flow_curr), 1])
        for i in range(len(self.data_flow_curr)):
            data_time[i] = float(self.data_sim[i][0])

        ## Settings for plots
        fig, axes = plt.subplots(1,1, sharex=True)
        sup_title_font_size = 28    
        title_font_size = 24
        label_font_size = 22
        tick_font_size = 16
        legend_font_size = 22
        fig.suptitle("Open Channel Flow - Measured v Estimated", fontsize=sup_title_font_size)
        axes.set_xlabel("Time [days]", fontsize=label_font_size)
        axes.set_ylabel("Flow [m^3/s]", fontsize=label_font_size)

        ## Plot data
        curr = axes.plot(data_time[:-2], self.data_flow_curr[:-2], '-', label="estimated flow", linewidth=3)
        ##prev = axes.plot(data_time[:-2], self.data_flow_prev[:-2], ':', label="previous flow estimate", linewidth=3) ## For testing
        meas = axes.plot(data_time[:-2], self.data_flow_meas[:-2], '-', label="measured flow ", linewidth=3)
        plt.legend(fontsize=legend_font_size)
        plt.show()


if __name__ == "__main__":
    ## Load user settings
    parser = argparse.ArgumentParser(description='Plot estimated flow.')
    args = parser.parse_args()

    print ("Plotting OCF - Filter Results!")

    ## Build Data object
    data = Data()
    data.load_data()
    data.plot()
