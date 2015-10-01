"""
Performs a simulation set.
The following parameters are constant and shared between all
simulations:
    -number of racks (2)
    -number of servers per rack (32)
    -number of users (1)
The only varying parameter is the scheduler
"""

import sim
import time

class Simu:
	def __init__(self, scheduler, name):
		self.scheduler = scheduler
		self.name = name

def splitResultFile(filename):
	with open(filename, "r") as f:
		for line in f:
			yield line.split(' ')

def getdataEnergy(filename):
	serversEnergy = 0.0
	totalEnergy = 0.0
	with open(filename, "r") as f:
		for line in f:
			fields = line.split(' ')
			if fields[0] == "energy.servers":
				serversEnergy = float(fields[1])
			totalEnergy += float(fields[1])
	return (serversEnergy, totalEnergy)

def getdataTasks(filename):
	for (field, value) in splitResultFile(filename):
		if field == "tasks.total":
			return int(value)

def analyzeResults(filename, simulations):
	print("Results analysis...")
	with open(filename, "w") as f:
		f.write("Sheduler,Servers energy,Total energy,Task count\n")
		for simu in simulations:
			dataEnergyfilename = "trace/%s/energySummary.tr" % simu.name
			dataTasksfilename  = "trace/%s/taskSummary.tr" % simu.name
			serversEnergy, totalEnergy = getdataEnergy(dataEnergyfilename)
			taskCount = getdataTasks(dataTasksfilename)
			f.write("%s,%f,%f,%d\n" % (simu.scheduler, serversEnergy, totalEnergy, taskCount))
	print("Done!")

PREFIX = "Schedulers"

SCHED_NAMES = ["Green", "RoundRobin", "Random", "HEROS", "RandDENS", "BestDENS"]
RACK_COUNT = 2
SERVERS_PER_RACK = 32
USER_COUNT = 1

currenttime = int(time.time()*1000)

simus = [Simu(i, "%s_%d_%s" % (PREFIX, currenttime, i)) for i in SCHED_NAMES]

sim.ClearTraces(PREFIX)
for simu in simus:
	print("Processing %s..." % simu.name)
	sim.LaunchSim(simu.name, RACK_COUNT, SERVERS_PER_RACK, USER_COUNT, simu.scheduler)

analyzeResults("results/schedulers.csv", simus)

