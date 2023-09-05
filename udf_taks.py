from pyspark.sql import SparkSession
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType

# Create a Spark session
spark = SparkSession.builder.appName("CapitalizeWords").getOrCreate()

# Sample data
data = [("hello world",), ("python programming",), ("data science",)]
columns = ["text"]

# Create DataFrame
df = spark.createDataFrame(data, columns)

# Define UDF to capitalize each word
def capitalize_each_word(text):
    if text:
        return ' '.join([word.capitalize() for word in text.split()])
    else:
        return None

capitalize_udf = udf(capitalize_each_word, StringType())

# Apply UDF and create a new column
df = df.withColumn("capitalized_text", capitalize_udf(df["text"]))

# Show the DataFrame
df.show()

# Stop Spark session
spark.stop()
