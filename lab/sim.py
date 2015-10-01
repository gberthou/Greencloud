"""
Provides simple functions for simulation purposes
"""

import os

TRACEDIR_BASE = "lab/trace"

def LaunchSim(tracedir, rackcount, serversperrack, usercount, scheduler = "Green"):
	mainfile = "./run"
	absolutetracedir = "%s/%s" % (TRACEDIR_BASE, tracedir)
	command = "cd .. && %s -l -t=%s -rc=%d -spr=%d -u=%d -s=%s" % (mainfile, absolutetracedir, rackcount, serversperrack, usercount, scheduler)
	print(command)
	os.system(command)

def ClearTraces(prefix):
	os.system("rm -rf trace/%s_*" % prefix)
