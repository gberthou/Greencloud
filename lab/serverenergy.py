"""
Performs a simulation set.
The following parameters are constant and shared between all
simulations:
    -number of racks (1)
    -number of users (1)
The only varying parameter is the number of servers
"""

import sim
import time

class Simu:
	def __init__(self, servercount, name):
		self.servercount = servercount
		self.name = name

currenttime = int(time.time()*1000)

simus = [Simu(i, "ServerEnergy_%d_%d" % (currenttime, i)) for i in range(1, 10, 2)]

sim.ClearTraces()
for simu in simus:
	print("Processing %s..." % simu.name)
	sim.LaunchSim(simu.name, 1, simu.servercount, 1)

