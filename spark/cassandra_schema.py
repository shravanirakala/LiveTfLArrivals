from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import logging

def create_cassandra_schema():
    auth = PlainTextAuthProvider(username='cassandra', password='cassandra')
    cluster = Cluster(['cassandra'], auth_provider=auth)
    session = cluster.connect()

    session.execute("""
    CREATE KEYSPACE IF NOT EXISTS tfl_arrivals 
    WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
    """)

    session.execute("""
    CREATE TABLE IF NOT EXISTS tfl_arrivals.ksx(
        id UUID PRIMARY KEY,
        tfl_id TEXT,
        mode_name TEXT,
        station_name TEXT,
        platform_name TEXT,
        towards TEXT,
        timestamp TIMESTAMP,
        time_to_station INT,
        expected_arrival TIMESTAMP
    )
    """)
    session.shutdown()
    logging.info("Cassandra schema is ready")