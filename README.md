Open Channel Flow - Kalman Filters

1) Generate simulation data with:
 `python3 [duration, secs] [timestep, secs] [num_cycles] [channel width, m] [bank_angle, deg] [initial speed, m/s] [water height, m]`.
2) Run Kalman Filter with:
 `./flow`
3) Plot results with: 
`python3 data_plot.py ocf_meas.csv ocf_prev.csv ocf_curr.csv ocf_data.csv`