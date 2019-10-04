#!/usr/bin/env python

# Import the necessary modules needed for the program

import socket
import time
import threading
import os
import argparse

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

flag_parser.add_argument('-n', dest='net', action='store', help='Provide the first three octets of the network you would like to scan')
flag_parser.add_argument('-s', dest='stn', action='store', help='Provide the first number of the network you would like to scan')
flag_parser.add_argument('-e', dest='en', action='store', help='Provide the last number of the network you would like to scan')

# Define variable arguments for Port scan

flag_parser.add_argument('-ps', '--pscan', action='store_true', help='This flag will enable port scan options')
flag_parser.add_argument('-sp', dest='sport', action='store', help='Provide the starting port number you would like to scan')
flag_parser.add_argument('-ep', dest='eport', action='store', help='Provide the ending port you would like to scan')

flags = flag_parser.parse_args()

if flags.pscan:
	pscan = True

# Define other required variables

a = '.'
stnum = int(flags.stn)
end = int(flags.en)
end = end+1

ping1 = 'ping -c 1 '

# Create list for IP randomization

ips = []
up = []

# Push all options for last octet of IP to list

for i in range(stnum, end, 1):
	ips.append(i)

# Shuffle the list for randomization

shuffle(ips)

# Define Start time

t1 = datetime.now()

os.system('clear')
print (C+"Scanning in progress...")

# Conduct randomized ping sweep

for ip in ips:
	addr = flags.net + a + str(ip)
	icmp = ping1 + addr
	response = os.popen(icmp)

	for line in response.readlines():
		if (line.count("ttl")):
			up.append(addr)
			print ""
			print G+"[+]"+W+" -->  " +G+ addr +W+ " is UP"

t2 = datetime.now()

total = t2 - t1

print ""
print T+"Host discovery complete"
print ""
print "Total time for host discovery: ", total
print ""

def portdata():

# Define required variables
	if flags.sport:
		stport = int(flags.sport)

	if flags.eport:
		enport = int(flags.eport)
		enport = enport+1

	# Create list of ports for randomization

	ports = []

	# Push all options for ports to list

	for p in range(stport, enport, 1):
		ports.append(p)

	# Shuffle the list of ports for randomization

	shuffle(ports)

	for ip in up:
		t_IP = socket.gethostbyname(ip)
		print C+"Starting scan on host: ", R+t_IP
		print ""

		for port in ports:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				conn = sock.connect_ex((t_IP, port))
				if conn == 0:
					print G+"[+]" +W+ " PORT " +G+ "{}".format(port) +W+ " is OPEN\n"
				conn.close()
			except:
				pass


if pscan == True:
	pt1 = datetime.now()
	print B+"Beginning Port scan..."
	print ""
	portdata()
	pt2 = datetime.now()
	ptotal = pt2 - pt1
	print O+"Total port scan time : ", ptotal


