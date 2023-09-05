from pyspark import SparkConf
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("StorageCheck").getOrCreate()
sc=spark.sparkContext
conf = SparkConf().setAppName("StorageCheck")
# sc = sc(conf=conf)

default_fs = sc._jsc.hadoopConfiguration().get("fs.defaultFS")

if default_fs.startswith("file:"):
    print("Spark is using local storage.")
elif default_fs.startswith("hdfs:"):
    print("Spark is using HDFS.")
else:
    print(f"Spark is using a custom filesystem: {default_fs}")
