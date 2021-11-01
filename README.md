# capstone_project

Project Overview:
Design complete solution to demonstrate end-to-end pipeline development and manage a machine/deep learning project
Develop an understanding of all stages of a machine learning project life-cycle
Demonstrate understanding of challenges encountered during the project development and provide ways to tackle them
Showcase understanding of software engineering best practices while developing the project

Problem Statement:
Classify News Articles into categories - With information overload today users are inundated with news articles of all topics, even the ones which may not be relevant to users. Design a system which can classify incoming news articles and appropriately tag the corresponding category. Develop a data pipeline which includes the all the following stages of Machine Learning Project Life Cycle – 
1.Data Ingestion
2.Data Preparation
3.Data segregation & Model Training
4.Model Deployment
5.Model Prediction

Project Milestones:

1. Data Ingestion
2. Data Cleansing & Preparation
3. Data Segregation & Model Training
4. Model Deployment
5. Model Prediction


Run below commands on docker host.

1. docker-compose up
2. docker-compose exec mongo1 /usr/bin/mongo --eval '''if (rs.status()["ok"] == 0) { rsconf = { _id : "rs0", members: [ { _id : 0, host : "mongo1:27017", priority: 1.0 } ] }; rs.initiate(rsconf); } rs.conf();'''
3. curl localhost:8083/connector-plugins | jq
4. curl http://localhost:8083/connectors/mongo-sink/status | jq
5.curl -X POST -H "Content-Type: application/json" -d @sink-connector.json http://localhost:8083/connectors | jq
6. curl localhost:8083/connector-plugins | jq
7. docker-compose exec broker bash
8. kafka-topics --zookeeper zookeeper:2181 --create --topic capstone.news_articles --partitions 1 --replication-factor 1
9. You can access the UI at http://host_ip:8501/ You can access the swagger ui at http://host_ip:8889/

Steps for Monolithic code:
1. Run kafka zookeeper service.
2. Run kafka server start i.e. brokerr start.
3. Create topic news_articles.
4.Run api_data_publisher.py in one terminal.
5.Run feed_data_publisher.py in one terminal.
6.Run main.py in another terminal for swagger UI.
7.Run streamlit run streamlit_ui.py for UI in another terminal.
8. You can access the UI at http://host_ip:8501/ You can access the swagger ui at http://host_ip:8889/
