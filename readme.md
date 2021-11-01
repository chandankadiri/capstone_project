# Setting up Environment:

### Steps for Dockerized code:
Run below commands on docker host.
- docker-compose up
- docker-compose exec mongo1 /usr/bin/mongo --eval '''if (rs.status()["ok"] == 0) {
       rsconf = {
         _id : "rs0",
         members: [
           { _id : 0, host : "mongo1:27017", priority: 1.0 }
         ]
       };
       rs.initiate(rsconf);
   }
   rs.conf();'''
- curl localhost:8083/connector-plugins | jq
- curl http://localhost:8083/connectors/mongo-sink/status | jq
- curl -X POST -H "Content-Type: application/json" -d @sink-connector.json http://localhost:8083/connectors | jq
- curl localhost:8083/connector-plugins | jq
- docker-compose exec broker bash
- kafka-topics --zookeeper zookeeper:2181 --create --topic capstone.news_articles --partitions 1 --replication-factor 1

You can access the UI at http://<your host ip>:8501/
You can access the swagger ui at http://<your host ip>:8889/

### Steps for Monolithic code:

- Run kafka zookeeper service.
- Run kafka server start i.e. brokerr start.
- Create topic news_articles.
- Run api_data_publisher.py in one terminal.
- Run feed_data_publisher.py in one terminal.
- Run main.py in another terminal for swagger UI.
- Rum streamlit run streamlit_ui.py for UI in another terminal.


You can access the UI at http://<your host ip>:8501/
You can access the swagger ui at http://<your host ip>:8889/

