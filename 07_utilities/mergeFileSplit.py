from pyspark.sql import SparkSession
from pyspark.sql.functions import col

# สร้าง SparkSession
spark = SparkSession.builder.appName("SplitByCategory").getOrCreate()

# โหลดไฟล์ JSON ที่รวมกันไว้แล้ว
df = spark.read.json("output/beautycare_category_cleaned_only_category")

# กรองเฉพาะที่ new_main_category ไม่เป็น null
df = df.filter(col("new_main_category").isNotNull())

# ดึงค่าทุก category ที่มีอยู่
categories = [row["new_main_category"] for row in df.select("new_main_category").distinct().collect()]

# แยกและบันทึกไฟล์ตาม category
for category in categories:
    category_df = df.filter(col("new_main_category") == category)
    save_path = f"output/split_by_category/{category.replace(' ', '_')}"
    category_df.write.mode("overwrite").json(save_path)

print("แยกไฟล์ตาม category สำเร็จแล้ว ✅")
