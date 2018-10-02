#coding: utf-8

import subprocess, string, ast

def get(host): # O método deve receber um host

		command = "ssh user@" + host + " 'free -m | grep Mem'" # Comando para obter informações de RAM do host remoto
		
		try:
			output = subprocess.check_output(command, shell=True)  # Recebe a saída do comando acima
			mem_info = string.split(output) # Transforma strings de valores separados por espaços em uma lista
			ram_usage = float(mem_info[2])/float(mem_info[1])*100 # Calcula o percentual de uso da RAM

		except subprocess.CalledProcessError:
			ram_usage = 0.0  # Caso o host não seja alcançado, o comando resultará erro, então o uso da RAM será zero

		return ram_usage