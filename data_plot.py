###################################################################################
# Author: Callum Tyler 2020
#
### Description
# Plots esimates open channel flow. 
#
### Instructions:
# `python3 data_plot.py [flow_meas_file] [flow_prev_file] [flow_curr_file] [sim_data_file]`
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
    def __init__(self, filename_meas, filename_curr, filename_prev, filename_sim):
    	## Initialise data
        self.filename_meas = filename_meas
        self.filename_curr = filename_curr
        self.filename_prev = filename_prev
        self.filename_sim = filename_sim
        self.data_flow_meas = []
        self.data_flow_curr = []
        self.data_flow_prev = []
        self.data_sim = []

    def load_data(self):
    	## Get current full path
        current_directory = os.getcwd()
        ## Load curr, meas, prev, sim data
        self.data_flow_curr = genfromtxt(current_directory + '/' + 'ocf_flow_curr.csv', delimiter=',')
        self.data_flow_prev = genfromtxt(current_directory + '/' + 'ocf_flow_prev.csv', delimiter=',')
        self.data_flow_meas = genfromtxt(current_directory + '/' + 'ocf_flow_meas.csv', delimiter=',')
        self.data_sim = genfromtxt(current_directory + '/' + 'ocf_data.csv', delimiter=',')

    def plot(self):
    	## Settings for plots
        fig, axes = plt.subplots(1,1, sharex=True)
        sup_title_font_size = 28	
        title_font_size = 24
        label_font_size = 20
        tick_font_size = 16
        legend_font_size = 18
        fig.suptitle("Flow estimates [m^3/s]", fontsize=sup_title_font_size)
        axes.legend(fontsize=legend_font_size)
        axes.set_xlabel("Time [sec]", fontsize=label_font_size)
        axes.set_ylabel("Flow [m^3/s]", fontsize=label_font_size)

        ## Prepare time data for plot
        data_time = np.empty([len(self.data_flow_curr), 1])
        for i in range(len(self.data_flow_curr)):
        	data_time[i] = float(self.data_sim[i][0])

        ## Plot data
        axes.plot(data_time, self.data_flow_curr, label="current flow estimate")
        axes.plot(data_time, self.data_flow_prev, label="previous flow estimate")
        axes.plot(data_time, self.data_flow_meas, label="measured flow estimate")
        plt.legend()
        plt.show()


if __name__ == "__main__":
	## Load user settings
	parser = argparse.ArgumentParser(description='Plot estimated flow.')
	parser.add_argument('flow_meas_file', help='input measured flow file')
	parser.add_argument('flow_prev_file', help='input previous flow file')
	parser.add_argument('flow_curr_file', help='input current flow file')
	parser.add_argument('sim_data_file', help='input simulated data file')
	args = parser.parse_args()

	## Build Data object
	data = Data(args.flow_meas_file, args.flow_prev_file, args.flow_curr_file, args.sim_data_file)
	data.load_data()
	data.plot()
