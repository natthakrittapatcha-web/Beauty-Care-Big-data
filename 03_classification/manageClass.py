from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode, count
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("Classify Review").getOrCreate()
df = spark.read.json("BeautyCare_joined_jsonl")

# คีย์เวิร์ดตามหมวดหมู่
keywords = {
    "Quality": [
        "good", "excellent", "bad", "poor", "effective", "soft", "smooth", "rough",
        "dandruff", "hair loss", "clean", "shiny", "healthy", "dry", "oily"
    ],
    "Packaging": [
        "bottle", "cap", "label", "appearance", "design", "branding", "color", "leak", "print"
    ],
    "Packing": [
        "box", "seal", "wrapped", "tape", "parcel", "delivery", "protection", "damaged", "bubble wrap"
    ]
}

# ฟังก์ชันจัดหมวดหมู่
def classify_review(text):
    if text is None:
        return "other"
    text = text.lower()
    scores = {}
    for label, words in keywords.items():
        scores[label] = sum(word in text for word in words)
    max_label = max(scores, key=scores.get)
    return max_label if scores[max_label] > 0 else "other"

# UDF สำหรับเลือก class หลัก
dominant_category_udf = udf(classify_review, StringType())

# เพิ่มคอลัมน์ tag ด้วยการวิเคราะห์ข้อความ
df = df.withColumn("tag", dominant_category_udf(col("text")))

# แสดงผลลัพธ์บางส่วน
df.select("text", "tag").show(truncate=False)

# เขียนกลับเป็นไฟล์ JSONL แบบมีหลายไฟล์ (หรือรวมเป็นไฟล์เดียวด้านล่าง)
df.write.mode("overwrite").json("output/beautycare_tag")

#df.coalesce(1).write.mode("overwrite").json("output/beautycare_with_tag_json_single")

