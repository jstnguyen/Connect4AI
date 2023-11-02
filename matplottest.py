
import matplotlib.pyplot as plt
import numpy as np

xpoints = np.array([1, 8])
ypoints = np.array([3, 10])

plt.subplot(1,2,1)
plt.plot(xpoints)
plt.xlabel("time")
plt.ylabel("losses")



plt.subplot(1,2,2)
plt.plot(ypoints)
plt.xlabel("time")
plt.ylabel("rewards")

plt.show()



# plt.plot(xpoints)
# plt.show()
#
# plt.plot(ypoints)
# plt.show()

# figure, axis = plt.subplots(1,2)
#
# axis[0,0].plot(xpoints)
# axis[0,0].set_title("losses")
#
# axis[0,1].plot(ypoints)
# axis[0,1].set_title("rewards")
#
# plt.show()