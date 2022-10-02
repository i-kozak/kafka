####Kafka job configuration steps
0. Download the project
0. Replace kafka-server-start.sh file within kafka/bin folder with the one downloaded. It has JMX server config replaced that is required to start 2nd and 3rd kafka broker
0. Upload server properties files to kafka/config folder
0. Upload py and create_topic.sh file into kafka folder
0. From kafka folder, start kafka brokers with the following commands (each require a separate session):<br>
`sudo JMX_PORT=9999 ./bin/kafka-server-start.sh config/server.properties`<br>
`sudo JMX_PORT=9998 ./bin/kafka-server-start.sh config/server1.properties`<br>
`sudo JMX_PORT=9997 ./bin/kafka-server-start.sh config/server2.properties`
0. Create a topic by running a `create_topic.sh` shell script
0. Start the nifi server
0. Apply the the nifi template downloaded
0. Install `python-kafka` for your venv
0. Start python code with `sudo python3 top_transactions.py`
0. Start all nifi processors
