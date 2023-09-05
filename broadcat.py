import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName('SparkByExamples.com').getOrCreate()

states = {"NY": "New York", "CA": "California", "FL": "Florida"}
broadcastStates = spark.sparkContext.broadcast(states)

data = [("James", "Smith", "USA", "CA"),
        ("Michael", "Rose", "USA", "NY"),
        ("Robert", "Williams", "USA", "CA"),
        ("Maria", "Jones", "USA", "FL")
        ]

columns = ["firstname", "lastname", "country", "state"]
df = spark.createDataFrame(data=data, schema=columns)

# Define a UDF to map state abbreviations to full names using the broadcast variable
def map_state(state):
    return broadcastStates.value[state]

map_state_udf = udf(map_state, StringType())

# Apply the UDF to the state column
df_with_full_state_names = df.withColumn("state", map_state_udf(col("state")))

df_with_full_state_names.printSchema()
df_with_full_state_names.show(truncate=False)
