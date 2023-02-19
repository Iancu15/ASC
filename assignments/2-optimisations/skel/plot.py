# Importing packages
import matplotlib.pyplot as plt

# Define data values
x = [160, 400, 600, 800, 1200, 1600]
y = [0.069, 1.135, 4.101, 9.466, 33.002, 87.974]
z = [0.021, 0.316, 1.054, 2.473, 8.352, 20.699]
w = [0.004, 0.038, 0.125, 0.277, 0.914, 2.141]

# Plot a simple line chart
plt.plot(x, y, 'g', label='neopt')

# Plot another line on the same chart/graph
plt.plot(x, z, 'r', label='opt')

plt.plot(x, w, 'b', label='blas')

plt.xlabel('N (matrix dimension)')
plt.ylabel('execution time (seconds)')

plt.legend()
plt.show()
