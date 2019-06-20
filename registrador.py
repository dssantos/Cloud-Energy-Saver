#coding: utf-8

import requests, header, ast, mac

def run():

	r = requests.get('http://controller:8774/v2.1/os-hypervisors', headers=header.get())
	hosts = ast.literal_eval(r.content) # Returns the content of the queried URL
	hosts = hosts['hypervisors']

	discovered = []

	for host in hosts:

		state = host['state']
		if state == 'up':
			hostname = host['hypervisor_hostname']
			discovered.append(hostname)
			mac.set(hostname)

	file = open("registered.txt", "w+")
	file.write(str(discovered)) # the discovered hosts are written to a file
	file.close()

	if len(discovered)>0:
		print '%s Registered Hosts!'%len(discovered)
	else:
		print '\nNo hosts found!\n'
	return discovered