from pyspark.sql import SparkSession
from pyspark.ml.feature import Tokenizer, StopWordsRemover, CountVectorizer
from pyspark.ml.clustering import LDA
from pyspark.sql.functions import udf, col
from pyspark.sql.types import ArrayType, StringType
from bs4 import BeautifulSoup
from pyspark.sql.types import StructType, StructField, StringType, FloatType, BooleanType, IntegerType

# สร้าง SparkSession
spark = SparkSession.builder.appName("LDA_Topic_Modeling").getOrCreate()

# โหลด JSON

schema = StructType([
    StructField("helpful_vote", IntegerType(), True),
    StructField("main_category", StringType(), True),
    StructField("parent_asin", StringType(), True),
    StructField("price", FloatType(), True),
    StructField("product_name", StringType(), True),
    StructField("rating", FloatType(), True),
    StructField("sentiment", StringType(), True),
    StructField("tag", StringType(), True),
    StructField("text", StringType(), True),
    StructField("title", StringType(), True),
    StructField("user_id", StringType(), True),
    StructField("verified_purchase", BooleanType(), True),
    StructField("new_main_category", StringType(), True)
])

df = spark.read.schema(schema).json("output/split_by_category")
#df.printSchema()
#df.show(5, truncate=False)
#print(df.columns)

# ทำความสะอาด HTML
def clean_html(text):
    return BeautifulSoup(str(text), "html.parser").get_text().strip()

# Register UDF
clean_html_udf = udf(clean_html, StringType())

# Apply UDF
df = df.withColumn("clean_text", clean_html_udf(col("text")))

df.select("text", "clean_text").show(5, truncate=False)

# Tokenize
tokenizer = Tokenizer(inputCol="clean_text", outputCol="words")
df = tokenizer.transform(df)

# ลบ stopwords
remover = StopWordsRemover(inputCol="words", outputCol="filtered_words")
df = remover.transform(df)

# Vectorize
vectorizer = CountVectorizer(inputCol="filtered_words", outputCol="features")
model = vectorizer.fit(df)
df = model.transform(df)

# LDA
lda = LDA(k=5, maxIter=10, featuresCol="features")
lda_model = lda.fit(df)

# คำนวณ topics
topics = lda_model.describeTopics(10)
vocab = model.vocabulary

# แปลง topic index เป็นคำ
def words_from_indices(indices):
    return [vocab[i] for i in indices]

words_udf = udf(words_from_indices, ArrayType(StringType()))
topics = topics.withColumn("top_words", words_udf(topics["termIndices"]))

# ✅ เขียนผลลัพธ์ลง CSV
topics.write.mode("overwrite").option("header", "true").csv("output/lda_topics")

print("✅ LDA topics saved to output/lda_topics")
