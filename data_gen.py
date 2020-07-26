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
# -> Surface width dependant on  water height.
# -> bank angle is measured from the horizon
# -> Steady-State, Uniform Flow in open channel
# -> Manning's roughness is concrete trowel finish
#
####################################################################################

import os
import csv
import random
import math
import argparse
import data_gen_params

class Data:
    ## Initialise class
    def __init__(self, _data_gen_params):
        ## initialise arrays, constants, variables
        self.channel_width = float(_data_gen_params._channel_width) ## channel width
        self.output_file = "data/ocf_data.csv" ## output file
        self.duration = float(_data_gen_params._duration) ## duration of data generation
        self.num_cycles = float(_data_gen_params._num_cycles) ## number of cyles
        self.step = float(_data_gen_params._timestep) ## time step
        self.depth = [float(_data_gen_params._inital_water_depth)] # water depth array
        self.width = [] # surface width array
        self.speed = [] # water speed array
        self.t_arr = [] ## time array
        self.angle_step = 2*math.pi/(self.duration/self.step)*self.num_cycles ## variation step
        self.bank_angle_vert = 90-float(_data_gen_params._bank_angle) ## bank angle from vertical
        self.num_decimals = 4 ## rounding
        self.manning_coef = _data_gen_params._manning_coef ## trowel finished
        self.channel_angle = _data_gen_params._channel_angle ## degrees
        self.channel_length = _data_gen_params._channel_length # metres
        self.channel_decent = self.channel_length*math.sin(self.channel_angle) ## metres
        self.channel_slope = self.channel_decent/(self.channel_length*math.cos(math.radians(self.channel_angle))) ## channel slope
        self.width_noise = 0.0
        self.depth_noise = 0.0
        self.speed_noise = 0.0

    ## Generate data
    def gen_data(self):
        t = 0.0 ## Set time to zero
        angle = 0.0 ## Set varying angle to zero

        print ("Generating data %")
        while t <= self.duration:
            ## Vary random signal noise
            self.depth_noise = random.randint(-10,100)/1e3
            self.width_noise = random.randint(-2,20)/1e3
            self.speed_noise = random.randint(-8,80)/1e3

            ## Generate vairation signal w/ sinusoid
            variation = 0.8 + (math.cos(7*angle) + math.sin(3*angle) + math.sin(4*angle) + math.cos(angle))/4

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
    parser = argparse.ArgumentParser(description=\
        'Welcome to data_gen for generating open channel flow data. Parameters can edited in "gen_data_params.py".')
    args = parser.parse_args()

    data = Data(data_gen_params)
    data.gen_data()
    data.save_data()
    ##data.save_input_parameters() ## Unused