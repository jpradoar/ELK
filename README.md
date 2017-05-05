<p align="center">
  <img src="https://github.com/jpradoar/ELK/blob/master/img.png"/><br>
</p>
# Plataform:
	SO:  	Debian 8.6
	Arch: 	64bits
	RAM: 	1Gb
	HDD: 	8Gb



# Logstash package
	https://artifacts.elastic.co/downloads/logstash/logstash-5.3.2.deb

# Elasticsearch package
	https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.3.2.deb

# Kibana package
 	https://artifacts.elastic.co/downloads/kibana/kibana-5.3.2-amd64.deb



# WEBSERVER - 192.168.2.136 

# Update system
	apt-get update

# Install apache2
	apt-get install apache2 -y

# Create a basic index
	echo "<html><h1>Webserver para ELK </h1></html>" >/var/www/html/index.html

# Add repo
	echo "# jessie backports" >>/etc/apt/sources.list
	echo "deb http://http.debian.net/debian jessie-backports main" >>/etc/apt/sources.list

# Update the system and install java
	apt-get update && apt-get install -y jessie-backports openjdk-8-jdk -y


# Check the version of java
	java -version
		openjdk version "1.8.0_121"



# Download the logstash on my webserver
	wget https://artifacts.elastic.co/downloads/logstash/logstash-5.3.2.deb
	dpkg --install logstash-5.3.2.deb 
		(Reading database ... 46103 files and directories currently installed.)
		Preparing to unpack logstash-5.3.2.deb ...
		Unpacking logstash (1:5.3.2-1) over (1:5.3.2-1) ...
		Setting up logstash (1:5.3.2-1) ...
		Using provided startup.options file: /etc/logstash/startup.options
		Successfully created system startup script for Logstash






# De todo el archivo de configuración solo tengo descomentado estos parametros:  
	(cat /etc/logstash/logstash.yml  | grep -v "#")
	path.data: /var/lib/logstash
	path.config: /etc/logstash/conf.d
	path.logs: /var/log/logstash



# Add a basic file to graficate apache logs
	#------------------INPUT------------------
	input {
	  file {
	    path => "/var/log/apache2/access.log"
	    start_position => "beginning"
	  }
	}
	#------------------FILTER------------------
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
	#------------------OUTPUT------------------
	output {
	 elasticsearch {
	   # Server donde tengo mi elasticsearch
	   hosts => ["http://192.168.2.138:9200/"]
	   index => "apache-%{+YYYY.MM.dd}"
	   document_type => "system_logs"
	 }
	 stdout { codec => rubydebug }
	}
	#------------------EOF------------------



# Execute logstash
	/usr/share/logstash/bin/logstash  -f /etc/logstash/conf.d


# Luego de unos instantes logstash inicia, y si accedemos a nuestro webserver por http  en el log nos tendria que mostrar algo similar a esto:
	{
	        "request" => "/",
	          "agent" => "\"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36\"",
	           "auth" => "-",
	          "ident" => "-",
	           "verb" => "GET",
	        "message" => "192.168.2.10 - - [04/May/2017:06:08:09 -0500] \"GET / HTTP/1.1\" 304 180 \"-\" \"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/53.0.2785.143 Chrome/53.0.2785.143 Safari/537.36\"",
	           "path" => "/var/log/apache2/access.log",
	       "referrer" => "\"-\"",
	     "@timestamp" => 2017-05-04T11:08:11.707Z,
	       "response" => "304",
	          "bytes" => "180",
	       "clientip" => "192.168.2.10",
	       "@version" => "1",
	           "host" => "0.0.0.0",
	    "httpversion" => "1.1",
	      "timestamp" => "04/May/2017:06:08:09 -0500"
	}


# ELASTICSEARCH - 192.168.2.138


# Install  
	apt-get update
	echo "# jessie backports" >>/etc/apt/sources.list
	echo "deb http://http.debian.net/debian jessie-backports main" >>/etc/apt/sources.list
	apt-get install -t jessie-backports openjdk-8-jdk
 
# Download 
 	wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.3.2.deb && dpkg--install elasticsearch-5.3.2.deb

# Enable service 
	systemctl enable elasticsearch.service


# In my case, I change of elasticsearch memory size. (I set it in 256Mb   ...I have a poor server :(
	sed -i 's/-Xms2g/-Xms256M/g' /etc/elasticsearch/jvm.options
	sed -i 's/-Xmx2g/-Xmx256M/g' /etc/elasticsearch/jvm.options

# Edit the elasticsearch.yml (uncoment: path.data, network.host, http.port)
	sed -i 's/#path.data: \/path\/to\/data/path.data: \/var\/lib\/elasticsearch /g' /etc/elasticsearch/elasticsearch.yml
	sed -i 's/#network.host: 192.168.0.1/network.host: 0.0.0.0/g' /etc/elasticsearch/elasticsearch.yml
	sed -i 's/#http.port: 9200/http.port: 9200/g' /etc/elasticsearch/elasticsearch.yml


# Cosas que modifique en elasticsearch.yml
	cat /etc/elasticsearch/elasticsearch.yml | grep -v "#"
		cluster.name: ElasticsearchSrv
		path.data: /var/lib/elasticsearch 
		network.host: 0.0.0.0 
		http.port: 9200


# KIBANA 

# Instalo
	apt-get update
	echo "# jessie backports" >>/etc/apt/sources.list
	echo "deb http://http.debian.net/debian jessie-backports main" >>/etc/apt/sources.list
	apt-get install -t jessie-backports openjdk-8-jdk

# Descargo
	wget https://artifacts.elastic.co/downloads/kibana/kibana-5.3.2-amd64.deb && dpkg--install kibana-5.3.2-amd64.deb




# Modifico
	sed -i 's/#server.host: "localhost"/server.host: 0.0.0.0/g' /etc/kibana/kibana.yml


# Cosas que modifique en kibana.yml
	cat /etc/kibana/kibana.yml |grep -v "#"
		server.host: 0.0.0.0
		server.name: "kibana"
		elasticsearch.url: "http://192.168.2.138:9200"
