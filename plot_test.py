import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt

array1 = np.array([1, 2, 3, 4, 5])
array2 = np.array([1, 2, 3, 4, 5])
array3 = np.empty([1000,1])
array4 = np.empty([1000,1])
array5 = np.empty([1000,1])

my_data = genfromtxt('ocf_flow_curr.csv', delimiter=',')
my_data1 = genfromtxt('ocf_data.csv', delimiter=',')
print(len(my_data1))
print(my_data1[0][0])

# for i in range(len(array3)):
# 	array3[i] = i
# 	array4[i] = i+1
# 	array5[i] = len(array3)-i

# fig, axes = plt.subplots(1,1, sharex=True)
# sup_title_font_size = 28	
# title_font_size = 24
# label_font_size = 20
# tick_font_size = 16
# legend_font_size = 18
# fig.suptitle("Flow estimates [m^3/s]", fontsize=sup_title_font_size)
# axes.legend(fontsize=legend_font_size)
# axes.set_xlabel("Time [sec]", fontsize=label_font_size)
# axes.set_ylabel("Flow [m^3/s]", fontsize=label_font_size)

# axes.plot(array3, array4, label="current flow estimate")
# axes.plot(array3, array5, label="meas flow estimate")
# axes.plot(array3, my_data, label="prev flow estimate")
# axes.plot(array3, my_data1[:][0], label="prev flow estimate")
# plt.legend()
# plt.show()