###################################################################################
# Author: Callum Tyler 2020
#
### Description
# This script generates simulation data of a flow through an open channel. 
# Water depth and speed would be measured from gauges. Channel width from
# satellite images. Simulated height, water depth and speed data are then
# saved to a csv file.
#
### Instructions
# To generate simulation data:
# `python3 [output_file] [duration, secs] [timestep, secs] [channel width, m] \
# [bank_angle, deg] [initial speed, m/s] [water height, m]`
#
### Definition: Open Channel Flow 
# Flow equals wetted area (WA) multiplied by water speed (WS)
# Q = WA*WS = WS*(channel_width*water_depth + 2*sin(90-bank_angle)) [m^3/s]
#
#         surface_width       /  bank_angle
#    ⊢--------------------⊣ _/___
#  \                        /
#   \----------------------/ ⊤
#    \                    /  |  water_depth
#     \__________________/   ⊥
#      ⊢----------------⊣
#        channel_width
#
### Assumptions:
# -> water speed may not increase w/ height & width. <- need to correct
# -> Surface width dependant on  water height.
# -> bank angle is measured from the horizon
#
####################################################################################

import csv
import random
import math
import argparse
import pandas as pd
import os 

class Data:
	## Initialise class
	def __init__(self, h0, channel_width, v0, duration, timestep, output_file, bank_angle):
		self.h0 = float(h0) #TODO could get rid of these
		self.channel_width = float(channel_width)
		self.v0 = float(v0)
		self.duration = float(duration)
		self.step = float(timestep)
		self.output_file = output_file
		self.angle_step = math.pi/(self.duration/self.step)
		self.h = [self.h0] 
		self.t_arr = [0.0]
		self.W = []
		self.v = [self.v0]
		self.bank_angle_vert = 90-float(bank_angle) 
	
	## Generate data
	def gen_data(self):
		t=0.0
		angle=0.0

		print ("Generating data %")
		while t <= self.duration:
			angle = 0.0
			## Water surface width
			water_width=2*self.h[-1]*math.tan(math.radians(self.bank_angle_vert))+self.channel_width
			## Initial water surface width
			self.W.append(round(water_width, 3))
			h_noise = random.randint(-10,100)/1e4
			W_noise = random.randint(-2,20)/1e4
			v_noise = random.randint(-8,80)/1e4
			variation = math.cos(angle)
			self.h.append(round(self.h[-1]*variation + h_noise, 3))
			self.W.append(round(self.W[-1]*variation + W_noise, 3))
			self.v.append(round(self.v[-1]*variation + v_noise, 3))
			self.t_arr.append(t)
			angle += self.angle_step
			t += self.step
		print ("Generated data.")

	## Save data to csv
	def save_data(self):
		with open(self.output_file, 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			##writer.writerow(['timestamp', 'height', 'width', 'velocity', 'bank_angle']) ## Leave csv headless
			for i in range(len(self.t_arr)):
				writer.writerow([self.t_arr[i],self.h[i],self.W[i],self.v[i], 90-self.bank_angle_vert])
		print ("Saved data to: ", self.output_file)

	## Save parameters
	def save_input_parameters(self):
		with open("gen_data_parameters.txt", 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=',')
			writer.writerow(['duration', self.duration])
			writer.writerow(['initial_water_height', self.h0])
			writer.writerow(['initial_flow', self.v0])
			writer.writerow(['timestep', self.step])
			writer.writerow(['channel_width', self.channel_width])
			writer.writerow(['channel_bank_angle', 90-self.bank_angle_vert])
			

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Generate channel flow data.')
	parser.add_argument('output_file', help='output data file')
	parser.add_argument('duration', help='time duration, s')
	parser.add_argument('timestep', help='timestep size, s')
	parser.add_argument('channel_width', help="width, m")
	parser.add_argument('bank_angle', help="angle of bank from horizontal, degrees")
	parser.add_argument('initial_flow', help="water speed, m/s")
	parser.add_argument('inital_water_height', help="water height, m")
	args = parser.parse_args()

	data = Data(args.inital_water_height, args.channel_width, args.initial_flow, args.duration, args.timestep, args.output_file, args.bank_angle)
	data.gen_data()
	data.save_data()
	data.save_input_parameters()
