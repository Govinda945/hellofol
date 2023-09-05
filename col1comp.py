from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *

# Create a Spark session
spark = SparkSession.builder.appName("Colcomp1").getOrCreate()

data1 = [(10,"Jack"), (15,"smith"), (25,"James")]
data2 = [(10, 20,1001,"Jack"), (15, 25,1002,"smith"), (25, 30,1003,"James1")]
columns_df1 = ["c1","c2"]
columns_df2 = ["c4","c5","c6","c7"]
df1 = spark.createDataFrame(data1, columns_df1)
df2 = spark.createDataFrame(data2, columns_df2)
# df1.show()
# df2.show()
df1_cols=df1.columns
df2_cols=df2.columns
matching_columns = []

for col1 in df1_cols:
    for col2 in df2_cols:
        diff_count = df1.select(col1).exceptAll(df2.select(col2)).count()
        if diff_count == 0:
            matching_columns.extend([col1,col2])

print("Matching columns:", matching_columns)
# Define an empty schema
empty_schema = StructType([])

# Create an empty DataFrame with the empty schema
df1.select(col("c1")).show()
empty_df = spark.createDataFrame([])
res_df=empty_df.select("c1",lit(df1.c1*1))
res_df.show()
# empty_df.withColumn(matching_columns[0],df1.select(col(matching_columns[0])))
# empty_df.show()
# for col_match in matching_columns:
#     if col_match in df1.columns:
#         empty_df.withColumn(col_match,df1.select(col(col_match)))
#     else:
#         empty_df.withColumn(col_match,df2.select(col(col_match)))
# empty_df.show()