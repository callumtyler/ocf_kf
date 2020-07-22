###################################################################################
# Author: Callum Tyler 2020
#
### Description
# Plots esimates open channel flow
#
###################################################################################

import csv
import random
import math
import argparse
import os
import matplotlib.pyplot as plt
# from array import *
import numpy as np

class Data:
    def __init__(self, filename_meas, filename_curr, filename_prev, filename_sim):
        self.filename_meas = filename_meas
        self.filename_curr = filename_curr
        self.filename_prev = filename_prev
        self.filename_sim = filename_sim
        self.data_flow_meas = []
        self.data_flow_curr = []
        self.data_flow_prev = []
        self.data_sim = []

    def load_data(self):
        current_directory = os.getcwd()
        ## Load curr data
        with open(current_directory + '/' + self.filename_curr) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data_flow_curr.append(row)
        ## Load meas data
        with open(current_directory+ '/' +self.filename_meas) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data_flow_meas.append(row)
        ## Load prev data
        with open(current_directory+ '/' +self.filename_prev) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data_flow_prev.append(row)
        ## Load simulated time data
        with open(current_directory+ '/' +self.filename_sim) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.data_sim.append(row)

    def plot(self):
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

        data_time = np.empty([len(self.data_flow_curr), 1])
        for i in range(len(self.data_flow_curr)):
        	data_time[i] = float(self.data_sim[i][0])

        axes.plot(data_time, self.data_flow_curr, label="current flow estimate")
        axes.plot(data_time, self.data_flow_prev, label="previous flow estimate")
        axes.plot(data_time, self.data_flow_meas, label="measured flow estimate")
        plt.show()


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Plot estimated flow.')
	parser.add_argument('flow_meas_file', help='input measured flow file')
	parser.add_argument('flow_prev_file', help='input previous flow file')
	parser.add_argument('flow_curr_file', help='input current flow file')
	parser.add_argument('sim_data_file', help='input simulated data file')
	args = parser.parse_args()

	data = Data(args.flow_meas_file, args.flow_prev_file, args.flow_curr_file, args.sim_data_file)
	data.load_data()
	data.plot()
