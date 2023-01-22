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
from pyspark.sql.functions import split, col, explode, lower, regexp_extract
# %%
lines = words.select(split(col('value'), ' ').alias('Line'))
# %%s
words_ex = lines.select(explode(col('Line')).alias('Word'))
# %%
words_lower = words_ex.select(lower(col('Word')).alias('Words_Lower'))
# %%
words_clean = words_lower.select(regexp_extract(col('Words_Lower', ),'[a-z]*',0).alias('word'))
# %%
words_nonull = words_clean.where(col('word')!='')
# %%
result = words_nonull.groupBy(col('word')).count()
# %%
result.orderBy(col('count'), ascending=False).show(10)
# %%
result.orderBy(col('count').desc()).show(10)
# %%

# %%
result.write.csv('data/count_words.csv')
# %%
result.coalesce(1).write.csv('data/count_words2.csv')
# %%
import pyspark.sql.functions as F

final_result = (
    spark.read.text('data/gutenberg_books/1342-0.txt')
    .select(F.split(F.col('value'), ' ').alias('Line'))
    .select(F.explode(F.col('Line')).alias('Word'))
    .select(F.lower(F.col('Word')).alias('Words_Lower'))
    .select(F.regexp_extract(F.col('Words_Lower', ),'[a-z]*',0).alias('word'))
    .where(F.col('word')!='')
    .groupBy(F.col('word')).count()
)
final_result.orderBy(col('count').desc()).show(10)

# %%
import pyspark.sql.functions as F

final_result = (
    spark.read.text('data/gutenberg_books/*.txt')
    .select(F.split(F.col('value'), ' ').alias('Line'))
    .select(F.explode(F.col('Line')).alias('Word'))
    .select(F.lower(F.col('Word')).alias('Words_Lower'))
    .select(F.regexp_extract(F.col('Words_Lower', ),'[a-z]*',0).alias('word'))
    .where(F.col('word')!='')
    .groupBy(F.col('word')).count()
)
final_result.orderBy(col('count').desc()).show(10)

# %%
