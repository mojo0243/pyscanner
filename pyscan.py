#!/usr/bin/env python

# Import the necessary modules needed for the program

import socket
import time
import os
import argparse
import ipaddress
import multiprocessing

from datetime import datetime
from random import shuffle

# Define colors for screen 

W  = '\033[0m'  # white (normal)
R  = '\033[31m' # red
G  = '\033[32m' # green
O  = '\033[33m' # orange
B  = '\033[36m' # blue
C  = '\033[34m' # cyan
T  = '\033[93m' # tan

pscan = False

# Define variables arguments for the program

flag_parser = argparse.ArgumentParser()

# Define variable arguments for ping sweep

flag_parser.add_argument('-n', dest='net', action='store', help='Provide the first network with cider you would like to scan EX: 192.168.1.0/24')

# Define variable arguments for Port scan

flag_parser.add_argument('-ps', '--pscan', action='store_true', help='This flag will enable port scan options')
flag_parser.add_argument('-d', dest='range', action='store', help='Provide a portrange to scan with a dash EX: 1-100')
flag_parser.add_argument('-uL', dest='userList', action='store', help='Provide a list of ports to scan seperated by a comma EX: 1,3,80,445,8080')

flags = flag_parser.parse_args()

if flags.pscan:
	pscan = True

# Define other required variables

ipNet = ipaddress.ip_network(unicode(flags.net), strict = False)

# Create list for IPs and multiprocessing

up = []
processes = []

# Create list for Ports and multiprocessing

up2 = []
portProcesses = []

# Conduct Ping Sweep

def ping(ip, up):
	response = os.popen('ping -c 1 -W 1 '+ip, 'r')
	rping = response.read()
	response.close()

	if "bytes from "+ip in rping:
		up.append(rping.split()[1])

# Conduct Port Scan

def portsweep(up2, port, openPorts):

	for ip in up2:
		t_IP = str(ip)

		try:
			sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			conn = sock.connect_ex((t_IP, port))

			if conn == 0:

				print G+"[+] "+W+"Port "+G+"{}".format(port)+W+" is open on "+T+t_IP
				print ""
		except:
			pass

def portdata(up2):

	plist = []

	if flags.range:
		portRange = flags.range.split('-')
		stport = int(portRange[0])
		enport = int(portRange[1])
		enport = enport+1

		for p in range(stport, enport, 1):
			plist.append(p)

	if flags.userList:
		portlist = flags.userList.split(',')
		for i in portlist:
			userPort = int(i)
			plist.append(userPort)

	shuffle(plist)

	with multiprocessing.Manager() as manager:
		openPorts = manager.list()

		for por in plist:
			port = por
			po = multiprocessing.Process(target=portsweep, args=[up2, port, openPorts])
			po.start()
			portProcesses.append(po)

		for pop in portProcesses:
			pop.join()

# Define Main function

def main():

	os.system('clear')
	print C+"Scanning in progress..."

	t1 = datetime.now()

	with multiprocessing.Manager() as manager:
		up = manager.list()

		for i in ipNet.hosts():
			ip = str(i)
			p = multiprocessing.Process(target=ping, args=[ip, up])
			p.start()
			processes.append(p)

		for process in processes:
			process.join()

		for t in up:
			print G+"[+] "+W+"  -->  " +G+ t +W+ "  is UP"

		up2 = up[:]

	t2 = datetime.now()
	total = t2 - t1

	print ""
	print T+"Host Discovery Complete"
	print ""
	print "Total time for host discovery: ", total
	print ""

	if pscan == True:
		pt1 = datetime.now()
		print B+"Beginning Port Scan..."
		print ""
		portdata(up2)
		pt2 = datetime.now()
		ptotal = pt2 - pt1
		print O+"Total port scan time: ", ptotal

if __name__ == "__main__":
	main()


