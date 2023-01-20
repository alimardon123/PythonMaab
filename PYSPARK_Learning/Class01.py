# %%
from pyspark.sql import SparkSession

spark = (
    SparkSession
    .builder
    .master("local[1]")
    .appName('Analyze English Words')
    .getOrCreate()
)    
# %%
words = spark.read.text('data/gutenberg_books/1342-0.txt')
words
# %%
words.printSchema()

# %%
words.show(5, truncate=False)
# %%
from pyspark.sql.functions import split, col, explode, lower
# %%
lines = words.select(split(col('value'), ' ').alias('Line'))
# %%s
words_ex = lines.select(explode(col('Line')).alias('Word'))
# %%
words_lower = words_ex.select(lower(col('Word')).alias('Words_Lower'))
# %%
