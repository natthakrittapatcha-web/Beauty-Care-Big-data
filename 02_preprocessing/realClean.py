import json

allowed_categories = {"All Beauty", "Health & Personal Care", "Premium Beauty"}

def remove_duplicate_keys(record):
    keys_to_keep = ["parent_asin", "title", "main_category", "categories", "price",]
    return {k: v for k, v in record.items() if k in keys_to_keep}

with open("/mnt/ceph/HPC3-67/B6602017/meta_BeautyCare.jsonl", "r", encoding="utf-8") as infile, \
     open("/mnt/ceph/HPC3-67/B6602017/meta_cleaned.jsonl", "w", encoding="utf-8") as outfile:
    for line in infile:
        record = json.loads(line)
        if record.get("main_category") in allowed_categories:
            clean_record = remove_duplicate_keys(record)
            json.dump(clean_record, outfile)
            outfile.write("\n")
