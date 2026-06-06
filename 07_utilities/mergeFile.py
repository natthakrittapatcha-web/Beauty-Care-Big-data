import os
import json

folder_path = "output/beautycare_category_cleaned_only_category"
merged_data = []

# loop อ่านทุกไฟล์ที่ลงท้ายด้วย .json
for filename in sorted(os.listdir(folder_path)):
    if filename.endswith(".json"):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                    merged_data.append(obj)
                except json.JSONDecodeError as e:
                    print(f"ข้ามบรรทัดใน {filename} เพราะ decode ไม่ได้: {e}")

# บันทึกออกเป็น JSON แบบ array
output_path = "merged_reviews.json"
with open(output_path, "w", encoding="utf-8") as out_file:
    json.dump(merged_data, out_file, ensure_ascii=False, indent=2)

print(f"รวมทั้งหมด {len(merged_data)} รายการในไฟล์ {output_path}")