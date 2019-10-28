__How to start the iotproducer container__

Open a terminal window and execute the following commmands:
> ssh root@idax29.svl.ibm.com

> cd dashdb_analytic_tools/

> cd dashdblocal_notebooks/

> cd iot_producer

> ls

Here we see the Dockerfile in the iot_producer folder.

Build the docker image:
> docker build -t iotproducer .

Run the container:
> docker run --net=host -d --name=iotproducer iotproducer

Note : By default it writes 1000 messages and then it ends. You can change the number of messages written by specifying an integer number as parameter to the container, like: docker run --net=host -d --name=iotproducer iotproducer 5000

If you want to see the flow of data in your terminal:
> docker exec -it iotproducer kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic iot4dashdb --from-beginning

Note: if you have done this several time, a name conflict may appear, with a message like: *docker: Error response from daemon: Conflict. The container name "/iotproducer" is already in use by container "...". You have to remove (or rename) that container to be able to reuse that name.*
To address this issue, please run the following commands:
> docker stop iotproducer

> docker rm  iotproducer

Then you can continue with 
> docker run --net=host -d --name=iotproducer iotproducer

> docker exec -it iotproducer kafka/bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic iot4dashdb --from-beginning