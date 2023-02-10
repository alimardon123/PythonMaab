# %%
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window as W

spark = SparkSession.builder.appName('Puzzle').getOrCreate()

# %%
schema = T.StructType(
    [
        T.StructField('EmpId', T.IntegerType(), True),
        T.StructField('EmpName', T.StringType(), True),
        T.StructField('BirthDate', T.DateType(), True)
    ]
)
df = spark.read.csv('data/puzzle_003.csv', header=True,
                    schema=schema, dateFormat='dd-MM-yyyy')
df.show()
# %%
df.where((F.month(F.col('BirthDate')) == 5) & (
    F.dayofmonth(F.col('BirthDate')).between(7, 15))
).show()
# %%
