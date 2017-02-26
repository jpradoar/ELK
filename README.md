# ELK
<pre>

########### ELK ###############

Plataforma: CentOS 7
uname -a: Linux cliente 3.10.0-514.6.2.el7.x86_64 #1 SMP Thu Feb 23 03:04:39 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux
Firewall: No
Formato:  Virtual Machine (.vmdk)
Virtualizador: VirtualBox
Recursos de cada VM:
					CORE:  2 
					RAM:   4 Gb
					HDD:  10 Gb

Server:  ( Elastic + logstash + Kibana )


#################### install basics ##########################

Desabilito el selinux
	set enforce 0


Instalar net-tools para tener ifconfig y netstat (OPCIONAL)
	yum install net-tools vim mlocate -y 


Instalo Java (Elasticsearch requires Java 8 or later)
	yum install java-1.8.0-openjdk -y



###################### install elasticsearch #####################

Download and install the public signing key:
	rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch


Repo de elastic
	vim /etc/yum.repos.d/elasticsearch.repo
		[elasticsearch-5.x]
		name=Elasticsearch repository for 5.x packages
		baseurl=https://artifacts.elastic.co/packages/5.x/yum
		gpgcheck=1
		gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
		enabled=1
		autorefresh=1
		type=rpm-md


Instalo elastic
	yum install elasticsearch -y 


Relogueo y habilito el servicio
	systemctl daemon-reload && systemctl enable elasticsearch.service && service elasticsearch restart


Me aseguro que esté corriendo
	netstat -nltp | grep 127.0.0.1
		tcp        0      0 127.0.0.1:25            0.0.0.0:*               LISTEN      1493/master         
		tcp6       0      0 127.0.0.1:9200          :::*                    LISTEN      883/java            
		tcp6       0      0 127.0.0.1:9300          :::*                    LISTEN      883/java



################### install logstash #####################

Importo el GPG
	rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch


Agrego el repo
	vim /etc/yum.repos.d/logstash.repo
	[logstash-5.x]
	name=Elastic repository for 5.x packages
	baseurl=https://artifacts.elastic.co/packages/5.x/yum
	gpgcheck=1
	gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
	enabled=1
	autorefresh=1
	type=rpm-md


Instalo logstash
	yum install logstash -y 


Accedo al directorio de certificados
	cd /etc/pki/tls/


Una vez dentro, creo el certificado
	openssl req -subj '/CN=172.16.123.143/'  -x509 -days 3650 -batch -nodes -newkey rsa:2048 -keyout private/logstash-forwarder.key -out certs/logstash-forwarder.crt
	Generating a 2048 bit RSA private key
	............................................+++
	..........................................................................................................................+++
	writing new private key to 'private/logstash-forwarder.key'
	-----


Accedo al directorio del logstash
	cd /etc/logstash/conf.d/


Creo el archivo de configuración
	vim basic-config-httpd.conf	


input {
  file {
    path => "/var/log/httpd/access_log"
    start_position => "beginning"
  }
}

filter {
  if [path] =~ "access" {
    mutate { replace => { "type" => "apache_access" } }
    grok {
      match => { "message" => "%{COMBINEDAPACHELOG}" }
    }
  }
  date {
    match => [ "timestamp" , "dd/MMM/yyyy:HH:mm:ss Z" ]
  }
}

output {
  elasticsearch {
    hosts => ["localhost:9200"]
  }
  stdout { codec => rubydebug }
}
# EOF



Habilito el servicio de logstash
	systemctl enable logstash


Inicio el servicio de logstash
	service logstash start


Copio el certificado a mi server cliente  (del que voy a obtener logs)
	scp -r /etc/pki/tls/certs/logstash-forwarder.crt  root@172.16.123.144:/root/


Copio a mi cliente el rpm del logstash que bajé al principio
	scp -r logstash-5.2.1.rpm  root@172.16.123.144:/root/


Copio a mi cliente el rpm del java
	scp -r jdk-8u60-linux-x64.rpm  root@172.16.123.144:/root/



############# CLIENTE ##############

Copio el certificado que acabo de pasar
	cp logstash-forwarder.crt /etc/pki/tls/certs/


Instalo java
	yum localinstall jdk-8u60-linux-x64.rpm -y


Instalo el logstash
	yum localinstall logstash-5.2.1.rpm  -y 







######################## install kibana #######################

Importo el GPG
	rpm --import https://artifacts.elastic.co/GPG-KEY-elasticsearch


Agrego el repo
	vim /etc/yum.repos.d/kibana.repo
	[kibana-5.x]
	name=Kibana repository for 5.x packages
	baseurl=https://artifacts.elastic.co/packages/5.x/yum
	gpgcheck=1
	gpgkey=https://artifacts.elastic.co/GPG-KEY-elasticsearch
	enabled=1
	autorefresh=1
	type=rpm-md


Instalo kibana
	yum install kibana -y


Modifico el archivo de configuración para acceder desde cualquier host
		# Reemplazo este server.host: "localhost"  
		# Por este otro.  server.host: 0.0.0.0        
	sed -i 's/#server.host: "localhost"/server.host: 0.0.0.0/g' /etc/kibana/kibana.yml

	# en DEV
	#sed -i 's/#elasticsearch.url: "http:\/\/localhost:9200"/elasticsearch.url: "http:\/\/172.16.123.145:9200"/g' /etc/kibana/kibana.yml


Levanto el servicio de kibana
	service kibana start
		kibana started

Me aseguro que esté corriendo
	service kibana status
		kibana is running


Esta corriendo Ok.
	netstat -nltp | grep 127.0.0.1     
		tcp        0      0 127.0.0.1:5601          0.0.0.0:*               LISTEN      2274/node  


Desde el navegador accedo a kibana
	http://IP-del-server:5601/
























Helps:
https://www.elastic.co
http://docs.oracle.com/javase/8/docs/technotes/guides/install/linux_jdk.html#BJFJHFDD
</pre>
