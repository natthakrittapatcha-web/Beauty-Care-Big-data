import os

input_file = 'BeautyCare.jsonl'
output_folder = 'BeautyCare_split'
lines_per_file = 200000

# สร้างโฟลเดอร์ output
os.makedirs(output_folder, exist_ok=True)

with open(input_file, 'r', encoding='utf-8') as f:
    file_count = 0
    lines = []
    
    for i, line in enumerate(f, 1):
        lines.append(line)
        if i % lines_per_file == 0:
            output_file = os.path.join(output_folder, f'part_{file_count}.jsonl')
            with open(output_file, 'w', encoding='utf-8') as out_f:
                out_f.writelines(lines)
            lines = []
            file_count += 1

    # เขียนไฟล์สุดท้ายถ้ายังมีบรรทัดเหลือ
    if lines:
        output_file = os.path.join(output_folder, f'part_{file_count}.jsonl')
        with open(output_file, 'w', encoding='utf-8') as out_f:
            out_f.writelines(lines)

print(f" แบ่งไฟล์เสร็จแล้ว: {file_count + 1} ไฟล์")
