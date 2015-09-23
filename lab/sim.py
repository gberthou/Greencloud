"""
Provides simple functions for simulation purposes
"""

import os

TRACEDIR_BASE = "lab/trace"

def LaunchSim(tracedir, rackcount, serversperrack, usercount):
	mainfile = "./run"
	absolutetracedir = "%s/%s" % (TRACEDIR_BASE, tracedir)
	command = "cd .. && %s -l -t=%s -rc=%d -spr=%d -u=%d" % (mainfile, absolutetracedir, rackcount, serversperrack, usercount)
	print(command)
	os.system(command)

def ClearTraces():
	os.system("rm -rf trace/*")
