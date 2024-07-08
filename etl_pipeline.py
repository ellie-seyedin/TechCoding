import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, trim, lower, when
from pyspark.sql.types import StringType
from thefuzz import process

spark = SparkSession.builder \
    .appName("ETL Pipeline") \
    .config("spark.sql.warehouse.dir", "file:///C:/temp/spark-warehouse") \
    .config("spark.local.dir", "C:/temp/spark-temp") \
    .config("spark.jars.packages", "com.crealytics:spark.excel_2.12:0.13.5") \
    .config("spark.jars", "C:/path/to/postgresql-42.2.18.jar") \
    .getOrCreate()

def read_data(csv_path, xlsx_path):
    csv_data = spark.read.option("header", "true").csv(csv_path)
    xlsx_data = spark.read.option("header", "true").format("com.crealytics.spark.excel") \
        .option("useHeader", "true").option("inferSchema", "true").load(xlsx_path)
    return csv_data, xlsx_data

def clean_data(df):
    for col_name in df.columns:
        df = df.withColumnRenamed(col_name, col_name.strip().lower().replace(' ', '_'))
    return df

def match_and_merge(csv_data, xlsx_data):
    csv_data = clean_data(csv_data)
    xlsx_data = clean_data(xlsx_data)
    
    xlsx_data = xlsx_data.withColumn("company_id", col("company_id").cast(StringType()))

    csv_company_names = csv_data.select("company_name").rdd.flatMap(lambda x: x).collect()
    
    def fuzzy_match(name):
        match = process.extractOne(name, csv_company_names)
        if match and match[1] > 80:
            return csv_data.filter(col("company_name") == match[0]).select("company_id").collect()[0][0]
        else:
            return None

    fuzzy_match_udf = spark.udf.register("fuzzy_match_udf", fuzzy_match, StringType())

    xlsx_data = xlsx_data.withColumn("company_id", when(col("company_id").isNull(), fuzzy_match_udf(col("company_name"))).otherwise(col("company_id")))
    
    merged_data = csv_data.join(xlsx_data, on="company_id", how="outer")
    return merged_data

def load_data_to_postgresql(data, table_name, db_url, db_properties):
    data.write.jdbc(url=db_url, table=table_name, mode="overwrite", properties=db_properties)
    print(f"Data loaded into {table_name} table")

def etl_pipeline(csv_path, xlsx_path, db_url, db_properties):
    csv_data, xlsx_data = read_data(csv_path, xlsx_path)
    merged_data = match_and_merge(csv_data, xlsx_data)
    load_data_to_postgresql(merged_data, "companies", db_url, db_properties)

if __name__ == "__main__":
    csv_path = 'data/electricity-generation_emissions_sources_ownership.csv'  
    xlsx_path = 'data/companies.xlsx'
    db_url = '***'
    db_properties = {
        "user": "***",
        "password": "***",  
        "driver": "***"
    }
    
    etl_pipeline(csv_path, xlsx_path, db_url, db_properties)
