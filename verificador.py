#coding: utf-8

import time, sys, status, muda_estado, ast, mac

def run(lim_max, lim_med):
	
	hosts = status.get()
	ram = []
	running = []
	idle = []
	offline = []

	try:
		file = open("registered.txt", "r+")
		registered = file.read()	
		registered = ast.literal_eval(registered)
	except:
		print 'É preciso registrar os hosts do ambiente'
		registered = []

	for host in hosts:	# Inserts the hosts that are connected (and have VMs) in an list of actives
		if host['state'] == 'up':
			if host['vms'] > 0:
				running.append(host['hostname'])
				ram.append(host['ram']) # Captures memory consumption and inserts into a list

	for host in hosts: # Inserts hosts that are running (and do not have VMs) in a list of idlers
		if host['state'] == 'up':
			if host['vms'] == 0:
				idle.append(host['hostname'])

	for host in hosts: # Inserts hosts that are shut down (and registered) in an list of offline 
		if host['state'] == 'down':
			if host['hostname'] in registered:
				offline.append(host['hostname'])

	try:
		ram_avg = sum(ram) / len(ram) # Calculates an average of memory in use by active hosts
	except:
		ram_avg = 0
	
	print 'ativos: ' + str(running)
	print 'ociosos: ' + str(idle)
	print 'offline: ' + str(offline)
	print 'média de ram: %s' %ram_avg

## Logic of the management of the hosts to be turned on and off
	
	if ram_avg > lim_max:						## If RAM is above the maximum limit
		if len(idle) > 0:
			if len(idle) > 1:					## They keep 1 idle on and shut off others
				for i in range(len(idle)-1):	# Turn off all except 1
					print 'desligando %s' %idle[i+1]
					muda_estado.shutdown(idle[i+1])
		else:
			if len(offline) > 0:				# If there are offline hosts ...
				print 'ligando %s' %offline[0]
				muda_estado.wake(offline[0]) 			# Wake up the first offline host from the list
			else:
				print 'Não há mais hosts offline para ligar.\nO sistema está no limite!!!'
	else:
		if len(idle) > 0:
			if ram_avg >= lim_med:				## If RAM is between the medium and maximum limits
				for i in range(len(idle)-1):	# Turn off all except 1
					print 'desligando %s' %idle[i+1]
					muda_estado.shutdown(idle[i+1])
			else:
				if len(running) >= 1:		## If there is at least 1 active host
					for host in idle:				
						print 'desligando %s' %host
						muda_estado.shutdown(host)		# shut down all idle hosts
				else:								# Else...
					for i in range(len(idle)-1):	# Turn off all except 1
						print 'desligando %s' %idle[i+1]
						muda_estado.shutdown(idle[i+1])

def start(lim_max, lim_med):
		
	while True:

		print '\n\nVerificando Hosts...\n'
		run(lim_max, lim_med)

		for i in xrange(90,-1,-1):
		     print "  Próxima verificação: %3d\r"%i,
		     time.sleep(1)
		     sys.stdout.flush()

