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

	for host in hosts:	# Insere os hosts que estão ligados (e possuem VMs) em uma lista de ativos 
		if host['state'] == 'up':
			if host['vms'] > 0:
				running.append(host['hostname'])
				ram.append(host['ram']) # Captura os consumos de memória e insere em uma lista

	for host in hosts: # Insere os hosts que estão ligados, mas não possuem VMs, em uma lista de ociosos
		if host['state'] == 'up':
			if host['vms'] == 0:
				idle.append(host['hostname'])

	for host in hosts: # Insere os hosts que estão desligados (e estão registrados) em uma lista de offline
		if host['state'] == 'down':
			if host['hostname'] in registered:
				offline.append(host['hostname'])

	try:
		ram_avg = sum(ram) / len(ram) # Calcula a média de memória em uso dos hosts ativos
	except:
		ram_avg = 0
	
	print 'ativos: ' + str(running)
	print 'ociosos: ' + str(idle)
	print 'offline: ' + str(offline)
	print 'média de ram: %s' %ram_avg

## Lógica do gerenciamento dos hosts a serem ligados e desligados
	
	if ram_avg > lim_max:						## Se RAM estiver acima do limite máximo
		if len(idle) > 0:
			if len(idle) > 1:					## Mantêm 1 ocioso ligado, mas desliga os demais
				for i in range(len(idle)-1):	# Desliga todos menos 1
					print 'desligando %s' %idle[i+1]
					muda_estado.shutdown(idle[i+1])
		else:
			if len(offline) > 0:				# Se existir hosts offline ...
				print 'ligando %s' %offline[0]
				muda_estado.wake(offline[0]) 			# Acorda o primeiro host offline da lista
			else:
				print 'Não há mais hosts offline para ligar.\nO sistema está no limite!!!'
	else:
		if len(idle) > 0:
			if ram_avg >= lim_med:				## Se RAM estiver entre os limites médio e máximo
				for i in range(len(idle)-1):	# Desliga todos menos 1
					print 'desligando %s' %idle[i+1]
					muda_estado.shutdown(idle[i+1])
			else:
				if len(running) >= 1:		## Se houver pelo menos 1 host ativo
					for host in idle:				
						print 'desligando %s' %host
						muda_estado.shutdown(host)		# Desliga todos os hosts ociosos
				else:								# Senão...
					for i in range(len(idle)-1):	# Desliga todos menos 1
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

