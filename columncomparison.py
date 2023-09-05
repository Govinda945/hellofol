from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a Spark session
spark = SparkSession.builder.appName("ColumnComparison").getOrCreate()

# Sample data for df1 and df2
data1 = [(10,), (15,), (25,)]
data2 = [(10, 20), (15, 25), (25, 30)]
columns_df1 = ["column_to_compare"]
columns_df2 = ["column1", "column2"]

# Create DataFrames
df1 = spark.createDataFrame(data1, columns_df1)
df2 = spark.createDataFrame(data2, columns_df2)

# Column in df1 to compare with all columns in df2
column_to_compare = "column_to_compare"

# List of columns in df2
columns_to_compare_with = df2.columns

matching_columns = []

# Compare the specified column in df1 with all columns in df2
for column in columns_to_compare_with:
    diff_count = df1.select(column_to_compare).exceptAll(df2.select(column)).count()
    
    if diff_count == 0:
        matching_columns.append(column)

print("Matching columns:", matching_columns)
input("Please enter something")