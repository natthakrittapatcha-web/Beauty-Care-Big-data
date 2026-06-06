# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import pandas_udf, col

import pandas as pd
from pyspark.sql.types import StringType
from textblob import TextBlob

# สร้าง SparkSession
spark = SparkSession.builder.appName("SentimentAnalysis").getOrCreate()

# โหลดไฟล์ JSONL ที่มีคอลัมน์ "text"
df = spark.read.json("output/beautycare_tag_grouped_cleaned")

# ฟังก์ชันวิเคราะห์อารมณ์
@pandas_udf(StringType())
def get_sentiment(texts: pd.Series) -> pd.Series:
    return texts.fillna("").apply(lambda text: (
        "positive" if TextBlob(text).sentiment.polarity > 0.1 else
        "negative" if TextBlob(text).sentiment.polarity < -0.1 else
        "neutral"
    ))


# เพิ่มคอลัมน์ "sentiment"
df = df.repartition(8)  # หรือมากกว่านี้ถ้าเครื่องแรง
df = df.withColumn("sentiment", get_sentiment(col("text")))

# แสดงตัวอย่างผลลัพธ์
df.select("text", "tag", "sentiment").show(truncate=False)

# บันทึกผลลัพธ์เป็น JSONL (หนึ่ง object ต่อบรรทัด)
df.write.mode("overwrite").json("output/beautycare_sentiment")