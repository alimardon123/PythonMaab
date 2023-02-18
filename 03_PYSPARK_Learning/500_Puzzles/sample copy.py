# %%
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window as W

spark = SparkSession.builder.appName('Puzzle').getOrCreate()

# %%
df = spark.read.csv('data/puzzle_002.csv', header=True, inferSchema=True)
df.show()
# %%
