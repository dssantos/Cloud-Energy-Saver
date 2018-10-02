#coding: utf-8

import requests, ast, os, time

def get():

	domain = 'Default'
	login = 'admin'
	password = '123456'
	project = 'admin'

	headers = {'Content-Type':'application/json'}
	body = """
	{
	    "auth": {
	        "identity": {
	            "methods": [
	            "password"
	            ],
	            "password": {
	                "user": {
	                    "domain": {
	                        "name": \""""+ domain +"""\"
	                    },
	                "name": \""""+ login +"""\",
	                "password": \""""+ password +"""\"
	                }
	            }
	        },
	        "scope": {
	            "project": {
	                "domain": {
	                    "name": \""""+ domain +"""\"
	                },
	                "name": \""""+ project +"""\"
	            }
	        }
	    }
	}
	"""

	now = time.time() # timestamp atual
	try:
		modified = os.path.getmtime('token.txt') # última modificação do arquivo
	except:
		modified = 0 # caso o arquivo não exista, modified será zero, assim entrará no else para gerar o token
	
	if now - modified < 3600:
		file = open("token.txt", "r+")
		header = file.read()

	else:
		r = requests.post('http://controller:5000/v3/auth/tokens', data=body, headers=headers)
		token = r.headers['X-Subject-Token']
		header = "{'X-Auth-Token':'"+token+"'}"  # Dicionário com o Token que será utilizado no cabeçalho das consultas via API
		file = open("token.txt", "w+")
		file.write(header)
		file.close()
		
	header = ast.literal_eval(header)  # Dicionário com o Token que será utilizado no cabeçalho das consultas via API

	return header