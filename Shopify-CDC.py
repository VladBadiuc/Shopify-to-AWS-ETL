# Databricks notebook source
from pyspark.sql.functions import when
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("CDC").getOrCreate()

# COMMAND ----------

load_df = spark.read.csv("/FileStore/tables/LOAD01.csv")
load_df = load_df.withColumnRenamed('_c0','First_name').withColumnRenamed('_c1','Last_name').withColumnRenamed('_c2','email')
load_df.write.mode("overwrite").csv("/FileStore/tables/Salida_CDC/final.csv")

# COMMAND ----------

new_df = spark.read.csv("/FileStore/tables/20221006_161745055__1_.csv")
new_df = new_df.withColumnRenamed('_c0','action').withColumnRenamed('_c1','First_name')
new_df = new_df.withColumnRenamed('_c2','Last_name').withColumnRenamed('_c3','email')

final_df = spark.read.csv("/FileStore/tables/Salida_CDC/final.csv")
#final_df = final_df.withColumnRenamed('_c0','action').withColumnRenamed('_c1','First_name')
final_df = final_df.withColumnRenamed('_c0','First_name').withColumnRenamed('_c1','Last_name').withColumnRenamed('_c2','email')

display(final_df)


# COMMAND ----------

for row in new_df.collect():
    if row['action'] == 'I':
        final_df = final_df.withColumn("First_name", when(final_df['email'] == row['email'], row['First_name']).otherwise(final_df['First_name']))
        final_df = final_df.withColumn("Last_name", when(final_df['email'] == row['email'], row['Last_name']).otherwise(final_df['Last_name']))
        
    if row['action'] == 'U':
        row_to_insert = list(row[1:])
        columns = ['First_name', 'Last_name', 'email']
        new_df = spark.createDataFrame(row_to_insert, columns)
        final_df = final_df.union(new_df)
        
    if row['action'] == 'D':
        final_df = final_df.filter(final_df.email != row['email'])
        
final_df.write.mode("overwrite").csv("/FileStore/tables/Salida_CDC/final.csv")

# COMMAND ----------


