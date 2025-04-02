# streamldn-kafka-spark
Realtime TfL Transport Pipeline Airflow-scheduled Kafka streaming with Spark processing, storing results in Cassandra

# Realtime Transport Data Pipeline  

- **Airflow**: Schedules and orchestrates TfL API data ingestion.  
- **Kafka**: Buffers real-time transport events (tube/bus delays).  
- **Spark**: Consumes and processes streaming data.  
- **Cassandra**: Stores processed data for low-latency queries.  
