from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# Create a Spark session
spark = SparkSession.builder.appName("ExtractColumns").getOrCreate()

# Sample data for df1 and df2
data1 = [("A", 10, 20), ("B", 15, 25), ("C", 30, 40)]
data2 = [("X", 5, 10), ("Y", 20, 30), ("Z", 35, 50)]
columns_df1 = ["id_df1", "column1_df1", "column2_df1"]
columns_df2 = ["id_df2", "column1_df2", "column2_df2"]

# Create DataFrames
df1 = spark.createDataFrame(data1, columns_df1)
df2 = spark.createDataFrame(data2, columns_df2)

# List of column names to extract
column_names = ["column1_df1", "column2_df2"]

# Extract columns from df1 and df2 with aliasing
selected_columns_df1 = df1.select(*[col(col_name).alias("selected_" + col_name) for col_name in column_names])
selected_columns_df2 = df2.select(*[col(col_name).alias("selected_" + col_name) for col_name in column_names])

# Show the extracted columns
selected_columns_df1.show()
selected_columns_df2.show()
