import pandas as pd
import random
from datetime import datetime, timedelta

# กำหนดสถานที่หลักในไทย
locations = [
    "สยามพารากอน", "สนามบินสุวรรณภูมิ", "สนามบินดอนเมือง", "ตลาดนัดจตุจักร", "เซ็นทรัลเวิลด์", 
    "อนุสาวรีย์ชัยสมรภูมิ", "ศูนย์ราชการแจ้งวัฒนะ", "สถานีขนส่งหมอชิต", "สถานีขนส่งเอกมัย", "สถานีหัวลำโพง"
]

# เทศกาลสำคัญ
festivals = ["สงกรานต์", "ปีใหม่", "ลอยกระทง", "เปิดเทอม", "ปิดเทอม", "วันหยุดนักขัตฤกษ์", "วันธรรมดา"]

# สุ่มช่วงเวลา
time_periods = ["06:00-09:00", "11:00-13:00", "17:00-20:00"]

# ฟังก์ชันสร้างข้อมูลสุ่ม
def generate_data(n=5000):
    data = []
    start_date = datetime(1999, 1, 1)
    end_date = datetime(2024, 12, 31)
    
    for _ in range(n):
        origin, destination = random.sample(locations, 2)
        date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        festival = random.choice(festivals)
        time_period = random.choice(time_periods)
        
        # กำหนดเวลาเดินทาง (สมมติ)
        base_time = random.randint(10, 60)  # เวลาเดินทางพื้นฐาน 10-60 นาที
        
        # ปรับค่าให้มี noise และความไม่สมบูรณ์
        if festival in ["สงกรานต์", "ปีใหม่"]:
            travel_time = base_time + random.randint(20, 90)  # รถติดหนัก
        elif festival == "เปิดเทอม" and time_period == "06:00-09:00":
            travel_time = base_time + random.randint(15, 60)  # รถติดตอนเช้า
        else:
            travel_time = base_time + random.randint(-5, 20)  # ปกติ
        
        # บางครั้งอาจมี missing values
        if random.random() < 0.01:
            travel_time = None
        
        data.append([origin, destination, date.strftime('%Y-%m-%d'), time_period, festival, travel_time])
    
    return pd.DataFrame(data, columns=["ต้นทาง", "ปลายทาง", "วันที่", "ช่วงเวลา", "เทศกาล", "ระยะเวลาเดินทาง (นาที)"])

# สร้าง DataFrame
df = generate_data(10000)  # 10,000 ตัวอย่าง

# บันทึกเป็น CSV
df.to_csv("traffic_dataset.csv", index=False, encoding='utf-8-sig')