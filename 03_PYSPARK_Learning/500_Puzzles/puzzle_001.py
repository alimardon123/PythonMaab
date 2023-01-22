#%%
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window as W

spark = SparkSession.builder.appName('Puzzle_01').getOrCreate()

# %%
schema = T.StructType(
    [
        T.StructField('BusinessEntityID', T.IntegerType(), True),
        T.StructField('SalesYear', T.IntegerType(), True),
        T.StructField('CurrentQuota', T.IntegerType(), True)
    ]
)
# %%
lag_df = spark.read.csv('data/Puzzle_001.csv', header=True, schema=schema)
# %%
lag_df.withColumn(
    'lagCurrentQuota',
    F.lag(F.col('CurrentQuota'),default=0).over(W.orderBy(F.lit(1)))   
).show()
# %%
lag_df.withColumn(
    'lagCurrentQuota',
    F.lag(F.col('CurrentQuota'),default=0).over(W.partitionBy(F.col('BusinessEntityID')).orderBy(F.lit(1)))   
).show()