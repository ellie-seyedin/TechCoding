import unittest
from pyspark.sql import SparkSession

class TestPostgreSQLConnection(unittest.TestCase):

    def setUp(self):
        self.spark = SparkSession.builder \
            .config("spark.jars", "C:/path/to/postgresql-42.2.18.jar") \
            .getOrCreate()

        self.jdbc_url = "***"
        self.connection_properties = {
            "user": "***",
            "password": "***",
            "driver": "***"
        }

    def tearDown(self):
        self.spark.stop()

    def test_postgresql_connection(self):
        try:
            df = self.spark.read.jdbc(url=self.jdbc_url, table="yourtable", properties=self.connection_properties)
            
            self.assertFalse(df.rdd.isEmpty(), "DataFrame is empty. Failed to read from PostgreSQL database.")
        
            self.assertGreater(df.count(), 0, "DataFrame is empty. Failed to read from PostgreSQL database.")
        except Exception as e:
            self.fail(f"Test failed with exception: {str(e)}")

if __name__ == '__main__':
    unittest.main()
