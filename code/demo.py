import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-4, 4, 100)
y = np.sin(x)

plt.scatter(x,y)
plt.xlabel('x')
plt.ylabel('y')
plt.show()