import pyspark
import nltk
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, array_contains, split
from pyspark.ml.feature import StopWordsRemover
from pyspark.ml.feature import Tokenizer
from pyspark.ml import Pipeline
from pyspark.ml.feature import CountVectorizer 
from pyspark.sql.functions import split, explode, regexp_replace, desc, lower
from pyspark.ml.feature import StopWordsRemover
from nltk.corpus import stopwords
#from pyspark.ml.feature import StandardScaler

spark = SparkSession.builder.master("local[*]").appName("projectao3").getOrCreate()

df = spark.read.csv("/home/madkins/example/all_munged_shortened_stories.csv", 
                    inferSchema=True, 
                    header=True, 
                    sep=",",  # You can try changing this to a different delimiter if needed.
                    quote='"',  # Make sure the correct quote character is used.
                    escape='"',  # Set the escape character if quotes are escaped inside cells.
                    multiLine=True)  # Enable multiline processing.

nltk.download('stopwords')
stop_words = stopwords.words('english')

stop_words = StopWordsRemover().getStopWords() + ["the", "because", "and", "to", "a", "an", "are", "as", "at", "be", "by", "for", "from", "has", "he", "she", "in", "is", "it", "its", "of", "on", "that", "to", "was", "were", "with", "like", "say", "back", "hey", "they",
"said", "one", "know", "re", "m", "get", "d", "says", "time", "eyes", "didn", "even", "going", "still"]

# GOOD PLACE WORD FILTER

# select the Story_Body column and remove null rows
df_filtered_gp = df.filter(col("Fandom") == "['The Good Place (TV)']")
df_cleaned_gp = df_filtered_gp.select("Story_Body").na.drop()

# remove special characters and lower the case
df_cleaned_gp = df_cleaned_gp.withColumn("cleaned_text", regexp_replace(df_cleaned_gp.Story_Body, '[^a-zA-Z\\s]', ''))
df_cleaned_gp = df_cleaned_gp.withColumn("cleaned_text", lower(df_cleaned_gp.cleaned_text))

# tokenize the text
tokenizer = Tokenizer(inputCol="cleaned_text", outputCol="words")
df_tokenized_gp = tokenizer.transform(df_cleaned_gp)

# remove stop words
remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)
df_filtered_gp = remover.transform(df_tokenized_gp)

# explode the filtered words
df_words_gp = df_filtered_gp.select(explode("filtered").alias("word")).filter(col("word") != '').filter(col("word") != ' ') # added. 

# count frequency of each word
df_frequency_gp = df_words_gp.groupBy("word").count()

# sort the words in descending order of their frequency
df_sorted_gp = df_frequency_gp.sort(desc("count"))

# display the top 10 most common words
print("The Good Place")
df_sorted_gp.show(10)

# BROOKLYN NINE-NINE WORD FILTER

# select the Story_Body column and remove null rows
df_filtered_b99 = df.filter(col("Fandom") == "['Brooklyn Nine-Nine (TV)']")
df_cleaned_b99 = df_filtered_b99.select("Story_Body").na.drop()

# remove special characters and lower the case
df_cleaned_b99 = df_cleaned_b99.withColumn("cleaned_text", regexp_replace(df_cleaned_b99.Story_Body, '[^a-zA-Z\\s]', ''))
df_cleaned_b99 = df_cleaned_b99.withColumn("cleaned_text", lower(df_cleaned_b99.cleaned_text))

# tokenize the text
tokenizer = Tokenizer(inputCol="cleaned_text", outputCol="words")
df_tokenized_b99 = tokenizer.transform(df_cleaned_b99)

# remove stop words
remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)
df_filtered_b99 = remover.transform(df_tokenized_b99)

# explode the filtered words
df_words_b99 = df_filtered_b99.select(explode("filtered").alias("word")).filter(col("word") != '').filter(col("word") != ' ')

# count frequency of each word
df_frequency_b99 = df_words_b99.groupBy("word").count()

# sort the words in descending order of their frequency
df_sorted_b99 = df_frequency_b99.sort(desc("count"))

# display the top 10 most common words
print("Brooklyn Nine-Nine")
df_sorted_b99.show(10)

# PARKS AND REC WORD FILTER

# select the Story_Body column and remove null rows
df_filtered_pnr = df.filter(col("Fandom") == "['Parks and Recreation']")
df_cleaned_pnr = df_filtered_pnr.select("Story_Body").na.drop()

# remove special characters and lower the case
df_cleaned_pnr = df_cleaned_pnr.withColumn("cleaned_text", regexp_replace(df_cleaned_pnr.Story_Body, '[^a-zA-Z\\s]', ''))
df_cleaned_pnr = df_cleaned_pnr.withColumn("cleaned_text", lower(df_cleaned_pnr.cleaned_text))

# tokenize the text
tokenizer = Tokenizer(inputCol="cleaned_text", outputCol="words")
df_tokenized_pnr = tokenizer.transform(df_cleaned_pnr)

# remove stop words
remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)
df_filtered_pnr = remover.transform(df_tokenized_pnr)

# explode the filtered words
df_words_pnr = df_filtered_pnr.select(explode("filtered").alias("word")).filter(col("word") != '').filter(col("word") != ' ')

# count frequency of each word
df_frequency_pnr = df_words_pnr.groupBy("word").count()

# sort the words in descending order of their frequency
df_sorted_pnr = df_frequency_pnr.sort(desc("count"))

# display the top 10 most common words
print("Parks and Rec")
df_sorted_pnr.show(10)

# THE OFFICE (US) WORD FILTER

# select the Story_Body column and remove null rows
df_filtered_off = df.filter(col("Fandom") == "['The Office (US)']")
df_cleaned_off = df_filtered_off.select("Story_Body").na.drop()

# remove special characters and lower the case
df_cleaned_off = df_cleaned_off.withColumn("cleaned_text", regexp_replace(df_cleaned_off.Story_Body, '[^a-zA-Z\\s]', ''))
df_cleaned_off = df_cleaned_off.withColumn("cleaned_text", lower(df_cleaned_off.cleaned_text))

# tokenize the text
tokenizer = Tokenizer(inputCol="cleaned_text", outputCol="words")
df_tokenized_off = tokenizer.transform(df_cleaned_off)

# remove stop words
remover = StopWordsRemover(inputCol="words", outputCol="filtered", stopWords=stop_words)
df_filtered_off = remover.transform(df_tokenized_off)

# explode the filtered words
df_words_off = df_filtered_off.select(explode("filtered").alias("word")).filter(col("word") != '').filter(col("word") != ' ')

# count frequency of each word
df_frequency_off = df_words_off.groupBy("word").count()

# sort the words in descending order of their frequency
df_sorted_off = df_frequency_off.sort(desc("count"))

# display the top 10 most common words
print("The Office")
df_sorted_off.show(10)

# HIGHLY VIEWED STORIES

#df_hits = df.select("Hits").na.drop()

# normalize the Kudos column using StandardScaler
#scaler = StandardScaler(inputCol="Hits", outputCol="scaled_hits", withMean=True, withStd=True)
#scaler_model = scaler.fit(df_hits)
#df_scaled_hits = scaler_model.transform(df_hits)

#df_filtered_hits = df_scaled_hits.filter(expr("abs(scaled_hits) > 3"))