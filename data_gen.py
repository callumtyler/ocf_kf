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
# `python3 [duration, secs] [timestep, secs] [num_cycles] [channel width, m] \
# [bank_angle, deg] [initial speed, m/s] [water height, m]`
# Generated data will be saved in "ocf_data.csv" in the directory of this script. 
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
# -> Steady-State, Uniform Flow in open channel
# -> Manning's roughness is trowel finish
#
####################################################################################

import os
import csv
import random
import math
import argparse

class Data:
    ## Initialise class
    def __init__(self, initial_depth, channel_width, initial_speed, duration, timestep, bank_angle, num_cycles):
        ## initialise arrays, constants, variables
        self.channel_width = float(channel_width) ## channel width
        self.output_file = "data/ocf_data.csv" ## output file
        self.duration = float(duration) ## duration of data generation
        self.num_cycles = float(num_cycles) ## number of cyles
        self.step = float(timestep) ## time step
        self.depth = [float(initial_depth)] # water depth array
        self.width = [float(channel_width)] # surface width array
        self.speed = [float(initial_speed)] # water speed array
        self.t_arr = [0.0] ## time array
        self.angle_step = 2*math.pi/(self.duration/self.step)*self.num_cycles ## variation step
        self.bank_angle_vert = 90-float(bank_angle) ## bank angle from vertical
        self.num_decimals = 4 ## rounding
        self.manning_coef = 0.013 # trowel finished #TODO my user input
        self.channel_angle = 1 # degrees #TODO my user input
        self.channel_length = 1000 # metres #TODO my user input
        self.channel_decent = 5 # metres #TODO my user input
        self.channel_slope = self.channel_decent/(self.channel_length*math.cos(math.radians(self.channel_angle))) # S_0
        self.width_noise = 0.0
        self.depth_noise = 0.0
        self.speed_noise = 0.0

    ## Generate data
    def gen_data(self):
        t = 0.0 ## Set time to zero
        angle = 0.0 ## Set varying angle to zero

        print ("Generating data %")
        while t <= self.duration:
            print (t)
            ## Vary random signal noise
            self.depth_noise = random.randint(0,100)/1e4 # Must be positive
            self.width_noise = random.randint(-2,20)/1e4
            self.speed_noise = random.randint(-8,80)/1e4

            ## Generate vairation signal w/ sinusoid
            variation = math.sin(angle) 

            ## Append depth calc. Use 1st value to allow sin variation. Must be calculated before speed & width
            self.depth.append(round(self.depth[0]*variation+self.depth_noise + self.depth[0], self.num_decimals))

            ## Calculate water speed
            self.calc_speed() 
            
            ## Calculate channel surface width
            self.calc_width() 

            ## Append time
            self.t_arr.append(round(t,self.num_decimals)) 
            
            ## Increment variation angle
            angle += self.angle_step 
            
            ## Increment time
            t += self.step 
        print ("Generated data.")

    ## Save data to csv
    def save_data(self):
        with open(self.output_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            ##writer.writerow(['timestamp', 'height', 'width', 'velocity', 'bank_angle']) ## Leave csv headless
            for i in range(len(self.t_arr)):
                writer.writerow([self.t_arr[i],self.depth[i],self.width[i],self.speed[i], 90-self.bank_angle_vert])
        print ("Saved data to: ", self.output_file)

    ## Save parameters
    def save_input_parameters(self):
        with open("gen_data_parameters.txt", 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',')
            writer.writerow(['duration', self.duration])
            writer.writerow(['initial_water_height', self.depth[0]])
            writer.writerow(['initial_flow', self.speed[0]])
            writer.writerow(['timestep', self.step])
            writer.writerow(['channel_width', self.channel_width])
            writer.writerow(['channel_bank_angle', 90-self.bank_angle_vert])

    ## Calculate water speed
    def calc_speed(self):
        wetted_perimeter = self.channel_width + 2*self.depth[-1]/math.cos(math.radians(self.bank_angle_vert)) ## wetted perimeter
        area = (self.depth[-1]**3)*(math.tan(math.radians(self.bank_angle_vert)) + self.channel_width) ## cross-sectional area
        hydraulic_radius = area/wetted_perimeter # hydraulic radius 
        curr_speed = ((hydraulic_radius**(2/3))*(self.channel_slope**(0.5)))/(self.manning_coef) + self.speed_noise ## current water speed
        self.speed.append(round(curr_speed, self.num_decimals)) ## Append speed calc.

    def calc_width(self):
        water_width=self.channel_width+2*self.depth[-1]*math.tan(math.radians(self.bank_angle_vert)) ## Use last value of depth
        self.width.append(round(water_width+self.width_noise, self.num_decimals)) ## Append width calc.
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate channel flow data.')
    parser.add_argument('duration', help='time duration, s')
    parser.add_argument('timestep', help='timestep size, s')
    parser.add_argument('num_cycles', help='number of sinusoid cycles')
    parser.add_argument('channel_width', help="width, m")
    parser.add_argument('bank_angle', help="angle of bank from horizontal, degrees")
    parser.add_argument('initial_flow', help="water speed, m/s")
    parser.add_argument('inital_water_height', help="water height, m")
    args = parser.parse_args()

    data = Data(args.inital_water_height, args.channel_width, args.initial_flow, args.duration, args.timestep, args.bank_angle, args.num_cycles)
    data.gen_data()
    data.save_data()
    data.save_input_parameters()

