#!/usr/bin/python
import os
import random
import time

# IP que uso para generar el request
RequestIP="192.168.2.136"

# Genero un numero random para la cantidad de request
request_num=random.randint(1,30)
# Genero un random de milisegundos para los request
def tiempo():
        for i in xrange(20):
                n = random.random()
                print "Milisegundos: " + str(n) + "\n"
                time.sleep(n)
                return

# Genero un bucle con una cantidad de loops random
for x in range(0, request_num): # Genero un loop con la cantidad de request que obtengo del request_num
        # genero una lista con index varios
        url_index = ['index.html', 'home.html', 'message.html', 'welcome.html', 'list.php', 'start.php', 'info.php', 'home.php', 'users.php', 'list_basic.php', ' ',]
        # Genero una lista con Agentes para los request
        agente = ['Mozilla/5.0', 'Chrome/4.1', 'Opera', 'Safari/1.2']
        # Guardo el request en una variable
        comando="curl -s -A "+(random.choice(agente))+" -XGET http://"+RequestIP+"/"+(random.choice(url_index))+" >/dev/null"
        # Creo un output para ver a donde le esta pegando el supuesto request
        output="http://"+RequestIP+"/"+(random.choice(url_index))
	# Ejecuto el request
        os.system(comando)
        # Imprimo la consulta que genera el request
        print output 
        # Llamo a la funcion de milisegundos para esperar entre cada request.
        tiempo()
#EOF
