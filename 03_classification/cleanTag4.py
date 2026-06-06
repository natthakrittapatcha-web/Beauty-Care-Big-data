# -*- coding: utf-8 -*-
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col, explode
from pyspark.sql.types import StringType

spark = SparkSession.builder.appName("BeautyCareTagGroupOnly").getOrCreate()

df = spark.read.json("output/beautycare_tag_grouped")

def map_tag_group(tag):
    if isinstance(tag, list):
        tag = tag[0] if tag else ""
    t = tag.lower() if tag else ""
    if any(k in t for k in ["quality", "effective", "performance", "result", "durability", "smooth", "long-lasting"]):
        return "Quality"
    elif any(k in t for k in ["packaging", "design", "box", "bottle", "presentation", "container"]):
        return "Packaging"
    elif any(k in t for k in ["packing", "shipping", "delivery", "wrap", "protection", "damaged"]):
        return "Packing"
    else:
        return "Other"

map_tag_udf = udf(map_tag_group, StringType())

if dict(df.dtypes)["tag"] == "array<string>":
    df = df.withColumn("tag", explode(col("tag")))

df = df.withColumn("tag_group", map_tag_udf(col("tag")))
df = df.filter(col("tag_group") != "Other")
df = df.drop("tag")

df.select("text", "tag_group").show(truncate=False)

df.write.mode("overwrite").json("output/beautycare_tag_grouped_cleaned_only_tag")
