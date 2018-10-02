#coding: utf-8

import subprocess, string, ast

def get(host):

	file = open("%s.txt"%host, "r+")
	macs = file.read()
	macs = ast.literal_eval(macs)
	return macs

def set(host):

	macs = []
	command1 = "ssh user@%s 'ls /sys/class/net'" %host

	try:
		list_intefaces = subprocess.check_output(command1, shell=True)
		list_intefaces = string.split(list_intefaces)

		for interface in list_intefaces:

			command = "ssh user@%s 'cat /sys/class/net/%s/address'" %(host, interface) # Comando para obter mac address
			mac = subprocess.check_output(command, shell=True)  # Recebe a saída do comando acima
			macs.append(mac.rstrip())     

	except subprocess.CalledProcessError:

		print 'Não foi possível obter o MAC de %s'%host


	file = open("%s.txt"%host, "w+")
	file.write(str(macs))
	file.close()

	print '%s %s'%(host, macs)