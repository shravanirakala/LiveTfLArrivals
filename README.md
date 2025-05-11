# Real-Time Streaming Data Pipeline for Transportation

Realtime TfL Transport(for London) Pipeline, using Airflow for scheduling, Kafka for streaming with Spark processing, and storing the results in Cassandra db.

# Streaming Data Architecture

- **Airflow**: Schedules and orchestrates the TfL API data ingestion pipeline.
- **PostgreSQL**: Backend metadata store for Airflow.
- **Kafka**: Broker for streaming data, Buffers real-time transport events (tubes and delays).  
- **Spark**: Consumes from Kafka, parses, and transforms messages.
- **Cassandra**: Stores the final processed data.
- **Docker Compose**: Orchestrates all services for local development.

# Project Structure

stream-tfl-to-cassandra/
│
├── dags/
│       └── kafka.py  # DAG to hit TFL API and push to Kafka
│       └── utils/
│                └── kafka_utils.py
│                └── tfl_api.py
│
├── spark/
│   ├── stream_to_cassandra.py        # Spark Streaming jobs
│   └── cassandra_schema.py           # creates Cassandra tables
│
├── docker-compose.yml                # Full pipeline with Airflow, Spark, Kafka, Cassandra
├── Dockerfile                        # Example env vars (like TFL API key, Kafka host)
├── requirements.txt                  # Python requirements
├── README.md                         # ← You’ll write this
└── LICENSE                           # (Optional) MIT/Apache license

# Start the Pipeline

# Trigger the Airflow DAG

# Run Spark Job

# Sample Outputs:


