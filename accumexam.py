from pyspark.accumulators import AccumulatorParam
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
spark = SparkSession.builder.appName("accumlator").getOrCreate()

type_of_drive = {"fwd":"front-wheel-drive","rwd":"rear-wheel-drive","4wd":"4wheel-drive"}
broadcastStates = spark.sparkContext.broadcast(type_of_drive)
class SumAccumulatorParam(AccumulatorParam):
    def zero(self, initialValue):
        return initialValue

    def addInPlace(self, v1, v2):
        return v1 + v2

# Create an accumulator with the custom accumulator param
accumulator = spark.sparkContext.accumulator(0, SumAccumulatorParam())

# Use the accumulator in transformations or actions
data=spark.read.csv("auto-data.csv",inferSchema=True,header=True)

def validate(row):
    if row.FUELTYPE=="diesel":
        accumulator.add(1)

data.foreach(lambda x:validate(x))

# Get the final value of the accumulator
result = accumulator.value
print("No of Vehicles using diesel type", result)

# Define a UDF to map state abbreviations to full names using the broadcast variable
def map_state(drive):
    return broadcastStates.value[drive]

map_state_udf = udf(map_state, StringType())

# Apply the UDF to the state column
df_with_full_drive_names = data.withColumn("DRIVE", map_state_udf(col("DRIVE")))

df_with_full_drive_names.printSchema()
df_with_full_drive_names.show(truncate=False)
print(df_with_full_drive_names.rdd.getNumPartitions())
df_repartition=df_with_full_drive_names.repartition(10)
df_repartition.write.csv("repartition_by_Make",header=True)
df_coalesce=df_repartition.coalesce(6)
df_coalesce.write.csv("coalesce_partition",header=True)