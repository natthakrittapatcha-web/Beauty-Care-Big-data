# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, count

# สร้าง Spark session
spark = SparkSession.builder \
    .appName("Find Duplicate categories") \
    .getOrCreate()

# อ่านไฟล์ JSONL
df = spark.read.json("/mnt/ceph/HPC3-67/B6602017/meta_cleaned.jsonl")

# ตรวจสอบ schema (ไม่บังคับ แต่แนะนำ)
df.printSchema()

category_counts = df.select(explode(col("categories")).alias("category")) \
    .groupBy("category") \
    .agg(count("*").alias("count")) \
    .orderBy(col("count").desc())

# แสดงผล
category_counts.show(truncate=False, n=1000)

# ปิด Spark session
spark.stop()