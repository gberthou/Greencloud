"""
Provides simple functions for simulation purposes
"""

import os

TRACEDIR_BASE = "lab/trace"

def LaunchSim(tracedir, rackcount, serversperrack, usercount, scheduler = "Green", load = 0.3):
	mainfile = "./run"
	absolutetracedir = "%s/%s" % (TRACEDIR_BASE, tracedir)
	command = "cd .. && %s -l -t=%s -rc=%d -spr=%d -u=%d -s=%s -lo=%f" % (mainfile, absolutetracedir, rackcount, serversperrack, usercount, scheduler, load)
	print(command)
	os.system(command)

def ClearTraces(prefix):
	os.system("rm -rf trace/%s_*" % prefix)

def SplitResultFile(filename):
	with open(filename, "r") as f:
		for line in f:
			yield line.split(' ')[0:2]

def GetdataEnergy(filename):
	serversEnergy = 0.0
	totalEnergy = 0.0
	for (field, value) in SplitResultFile(filename):
		if field == "energy.servers":
			serversEnergy = float(value)
		totalEnergy += float(value)
	return (serversEnergy, totalEnergy)
