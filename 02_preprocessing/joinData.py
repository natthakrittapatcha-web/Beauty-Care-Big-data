from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# สร้าง SparkSession
spark = SparkSession.builder.appName("BeautyCare Join Fix").getOrCreate()

# หมวดหมู่ที่อนุญาต
allowed_categories = {"All Beauty", "Health & Personal Care", "Premium Beauty"}

# อ่านไฟล์ meta ที่ path เต็ม
meta_raw = spark.read.option("multiline", "false").json("/mnt/ceph/HPC3-67/B6602017/meta_cleaned.jsonl")

# แก้ชื่อคอลัมน์ถ้ามีผิด
meta_fixed = meta_raw.withColumnRenamed("parent Asin", "parent_asin")

# กรองเฉพาะ main_category ที่อยู่ใน allowed_categories
meta_filtered = meta_fixed.filter(col("main_category").isin(allowed_categories))

# ตรวจสอบ schema
meta_filtered.printSchema()

# เลือกคอลัมน์ที่ต้องการ
meta_df = meta_filtered.select("parent_asin", col("title").alias("product_name"), "main_category", "categories", "price",)

# อ่าน review files ที่ path เต็ม
review_df = spark.read.option("multiline", "false").json("/mnt/ceph/HPC3-67/B6602017/BeautyCare_split")

# ตรวจสอบ schema
review_df.printSchema()

# เลือกเฉพาะคอลัมน์ที่ต้องการ
review_df = review_df.select("parent_asin", "title", "text", "rating", "user_id", "helpful_vote", "verified_purchase")

# Join โดยใช้ parent_asin
joined_df = meta_df.join(review_df,"parent_asin","inner")

# แสดงตัวอย่างผลลัพธ์
joined_df.show(5, truncate=False)

joined_df.coalesce(1).write.mode("overwrite").json("/mnt/ceph/HPC3-67/B6602017/BeautyCare_joined_jsonl")
