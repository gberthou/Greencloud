"""
Performs a simulation set.
The following parameters are constant and shared between all
simulations:
    -number of racks (1)
The varying parameters are the number of servers and the number of users
"""

import sim
import time

MIN_SERVER_COUNT  = 1
MAX_SERVER_COUNT  = 50
PACE_SERVER_COUNT = 4

MIN_USER_COUNT = 1
MAX_USER_COUNT = 10
PACE_USER_COUNT = 4

class Simu:
	def __init__(self, servercount, usercount, name):
		self.servercount = servercount
		self.usercount = usercount
		self.name = name

def analyzeResults(filename, simulations):
	print("Results analysis...")
	with open(filename, "w") as f:
		f.write("Server count,User count,Servers energy,Total energy\n")
		for simu in simulations:
			datafilename = "trace/%s/energySummary.tr" % simu.name
			serversEnergy, totalEnergy = sim.GetdataEnergy(datafilename)
			f.write("%d,%d,%f,%f\n" % (simu.servercount, simu.usercount, serversEnergy, totalEnergy))
	print("Done!")

currenttime = int(time.time()*1000)
PREFIX = "ServerUserEnergy"

simus = [Simu(i, j, "%s_%d_%d_%d" % (PREFIX, currenttime, i, j)) for j in range(MIN_USER_COUNT, MAX_USER_COUNT + 1, PACE_USER_COUNT) for i in range(MIN_SERVER_COUNT, MAX_SERVER_COUNT + 1, PACE_SERVER_COUNT)]

sim.ClearTraces(PREFIX)
for simu in simus:
	print("Processing %s..." % simu.name)
	sim.LaunchSim(simu.name, 1, simu.servercount, simu.usercount)

analyzeResults("results/serveruserenergy.csv", simus)
