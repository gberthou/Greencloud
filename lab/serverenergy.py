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

MIN_SERVER_COUNT  = 1;
MAX_SERVER_COUNT  = 200;
PACE_SERVER_COUNT = 4

class Simu:
	def __init__(self, servercount, name):
		self.servercount = servercount
		self.name = name

def analyzeResults(filename, simulations):
	print("Results analysis...")
	with open(filename, "w") as f:
		f.write("Server count,Servers energy,Total energy\n")
		for simu in simulations:
			datafilename = "trace/%s/energySummary.tr" % simu.name
			serversEnergy, totalEnergy = sim.GetdataEnergy(datafilename)
			f.write("%d,%f,%f\n" % (simu.servercount, serversEnergy, totalEnergy))
	print("Done!")

PREFIX = "ServerEnergy"

currenttime = int(time.time()*1000)

simus = [Simu(i, "%s_%d_%d" % (PREFIX, currenttime, i)) for i in range(MIN_SERVER_COUNT, MAX_SERVER_COUNT + 1, PACE_SERVER_COUNT)]

sim.ClearTraces(PREFIX)
for simu in simus:
	print("Processing %s..." % simu.name)
	sim.LaunchSim(simu.name, 1, simu.servercount, 1)

analyzeResults("results/serverenergy.csv", simus)
