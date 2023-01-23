# %%
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
import pyspark.sql.types as T
from pyspark.sql.window import Window as W

spark = SparkSession.builder.appName('Class_04').getOrCreate()
# %%
data = [
    [1, "John", "Tom", 2004, 250.5, 1],
    [2, "Jack", "Frank", 1999, 310.4, 1],
    [3, "Ann", "Joe", 2000, 450.0, 2],
    [4, "Mark", "Tven", 1999, 500.0, 3],
    [5, "Tom", "Cruz", 2001, 350.0, 5]
]
# %%
df = spark.createDataFrame(
    data=data, schema=["Id", 'Fname', 'Lname', 'Birth_Year', 'Salary', 'DeptId'])
# %%
select_cols = ['Id', 'Fname']
df.select(*select_cols).show()
# %%
df.withColumnRenamed('Fname', 'First_Name').show()
# %%
[x.lower() for x in df.columns]
# %%
df.toDF(*[x.lower() for x in df.columns]).show()
# %%
df.drop('Id', 'Salary').show()
# %%
df.show()
# %%
data2 = [
    [1, 'HR'],
    [2, 'IT'],
    [3, 'Marketing'],
    [4, 'Management']
]
employee = spark.createDataFrame(
    data=data2, schema=['DeptId', 'Department_Name'])

# %%
department = spark.createDataFrame(
    data=data, schema=["Id", 'Fname', 'Lname', 'Birth_Year', 'Salary', 'DeptId'])
# %%
employee.join(department, on=employee['DeptId'] == department['DeptId']).show()
# %%
employee.join(department, on='DeptId').show()
# %%
employee.alias('e').join(department.alias('d'), on=F.col(
    'e.DeptId') == F.col('d.DeptId')).show()
# %%
employee.alias('e').join(department.alias('d'), on=F.col(
    'e.DeptId') == F.col('d.DeptId'), how='left').show()
# %%
employee.alias('e').join(department.alias('d'), on=F.col(
    'e.DeptId') == F.col('d.DeptId'), how='full').show()
# %%
employee.alias('e').join(department.alias('d'), how='cross').show()
# %%
employee.crossJoin(department).show()
# %%
employee.alias('e').join(department.alias('d'), on=F.col(
    'e.DeptId') == F.col('d.DeptId'), how='left_semi').show()

# %%
employee.alias('e').join(department.alias('d'), on=F.col(
    'e.DeptId') == F.col('d.DeptId'), how='left_anti').show()
# %%
