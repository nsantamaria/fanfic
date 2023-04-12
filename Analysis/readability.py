import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import lit
import pandas as pd
from pyspark.sql import SQLContext
from pyspark.sql.types import *
import numpy as np
from readability import Readability



# Begin Spark Session
spark = SparkSession.builder.master("local[*]").appName("temp").getOrCreate()

# Modify the following line
df = spark.read.csv("/home/rlpatt/Project_01/parksandrec_punctuation.csv", 
                    inferSchema=True, 
                    header=True, 
                    sep=",",  # You can try changing this to a different delimiter if needed.
                    quote='"',  # Make sure the correct quote character is used.
                    escape='"',  # Set the escape character if quotes are escaped inside cells.
                    multiLine=True)  # Enable multiline processing.


# fandom = list(df.select("Fandom").toPandas()["Fandom"]) # => [1,2,3,4]
# print(fandom[0])


# Convert "Words" to strings
df = df.withColumn("Words", df.Words.cast(IntegerType()))

# Check
#df.printSchema()
#print(df.count())

# Get just the "Words" column
words = df.select("Words")
#print(words.collect()[0])

# Only choose stories with word count over 100
df_read = df.filter(df.Words > 100)
print(df_read.count())

# Select the story body 
df_story_body = df_read.select("Story_Body")
df_story_body.printSchema()

# df_story_body.withColumn("Story_Body", df.Story_Body.cast(StringType()))

# Convert story body df to rdd
story_rdd = df_story_body.rdd

print(type(story_rdd.take(1)))

# This it to transform each item in the body word list as a long string
story_strings = story_rdd.map(lambda x: "".join(x[0]))
print(story_strings.take(1))

# Readability package is on github. Several options avaliable.
r = story_strings.map(lambda x: Readability(x))
print(r.take(1))

# Flesch Kincaid Readability Metric - based on syllables, word length, sentence count/length, etc.
fleshkin = r.map(lambda x: x.flesch_kincaid())
print(fleshkin.take(1))

# Get the fk score for each story
scores = fleshkin.map(lambda x: x.score)
# print(type(scores))

# Get the scores out of a tuple
sdf = scores.map(lambda x: (x, )).toDF(["Scores"])
sdf.printSchema()
sdf.show(truncate=True)

# Get grade level for each story
levels = fleshkin.map(lambda x: x.grade_level)
print(type(levels.take(1)[0]))

# Get grade levels out of tuple
ldf = levels.map(lambda x: (x, )).toDF(["Levels"])
ldf.printSchema()
ldf.show(truncate=False)


# sdf.write.csv("parksandrec_fk_scores.csv")
# ldf.write.csv("parksandrec_grades.csv")
