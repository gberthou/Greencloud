"""
Performs a simulation set.
The following parameters are constant and shared between all
simulations:
    -total number of servers (64)
    -number of users         (1)
The only varying parameter is the scheduler
"""

import sim
import time

class Topology:
	def __init__(self, uniqueId, rackcount, serversperrack):
		self.uniqueId = uniqueId
		self.rackcount = rackcount
		self.serversperrack = serversperrack

class Simu:
	def __init__(self, scheduler, topology, load, name):
		self.scheduler = scheduler
		self.topology = topology
		self.load = load
		self.name = name

def getdataTasks(filename):
	for (field, value) in sim.SplitResultFile(filename):
		if field == "tasks.total":
			return int(value)
def getdataLoad(filename):
	for (field, value) in sim.SplitResultFile(filename):
		if field == "load.datacenter":
			return float(value)

def analyzeResults(filename, simulations):
	print("Results analysis...")
	with open(filename, "w") as f:
		f.write("Topo id, Rack count, Servers per rack, Effective load, Sheduler,Servers energy,Total energy,Task count\n")
		for simu in simulations:
			dataEnergyfilename = "trace/%s/energySummary.tr" % simu.name
			dataTasksfilename  = "trace/%s/taskSummary.tr"   % simu.name
			dataLoadfilename   = "trace/%s/loadSummary.tr"   % simu.name
			serversEnergy, totalEnergy = sim.GetdataEnergy(dataEnergyfilename)
			taskCount = getdataTasks(dataTasksfilename)
			dcLoad = getdataLoad(dataLoadfilename)
			f.write("%d,%d,%d,%.1f,%s,%.1f,%.1f,%d\n" % (simu.topology.uniqueId, simu.topology.rackcount, simu.topology.serversperrack, dcLoad, simu.scheduler, serversEnergy, totalEnergy, taskCount))
	print("Done!")

PREFIX = "Schedulers"

#SCHED_NAMES = ["Green", "RoundRobin", "Random", "HEROS", "RandDENS", "BestDENS"]
SCHED_NAMES = ["Green", "BestDENS", "HEROS", "RoundRobin", "Random"]
TOTAL_SERVERS = 64
RACK_COUNTS = [1, 2, 4]
LOADS = [i/10. for i in range(1,10)]
USER_COUNT = 1

"""
# To debug this script, you might want to uncomment the following instructions
SCHED_NAMES = ["Green"]
TOTAL_SERVERS = 16
RACK_COUNTS = [1]
LOADS = [0.8]
"""

currenttime = int(time.time()*1000)

topologies = [Topology(i, rackcount, TOTAL_SERVERS / rackcount) for i,rackcount in enumerate(RACK_COUNTS)]
simus = [Simu(sched, topo, load, "%s_%d_t%dx%d_l%f_%s" % (PREFIX, currenttime, topo.rackcount, topo.serversperrack, load, sched)) for topo in topologies for load in LOADS for sched in SCHED_NAMES]

sim.ClearTraces(PREFIX)
for simu in simus:
	print("Processing %s..." % simu.name)
	sim.LaunchSim(simu.name, simu.topology.rackcount, simu.topology.serversperrack, USER_COUNT, simu.scheduler, simu.load)

analyzeResults("results/schedulers.csv", simus)

