#%%
from pyspark.sql import SparkSession

spark = (
    SparkSession.builder.appName('SomeApp').getOrCreate()
)

import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window as W
# %%
data = [
    [1, "John", "Tom", 2004, 250.5],
    [2, "Jack", "Frank", 1999, 300.4],
    [3, "Ann", "Joe", 2000, 450.0]
]
# %%
df = spark.createDataFrame(data=data, 
    schema=['Id', 'Fname', 'Lname', 'Birth_Year', 'Salary'])
df.show()    
# %%
