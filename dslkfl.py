from pyspark.sql import SparkSession

# Create a Spark session
spark = SparkSession.builder.appName("StorageCheck").getOrCreate()

# Get the default filesystem
input("Please enter something")

spark.stop()