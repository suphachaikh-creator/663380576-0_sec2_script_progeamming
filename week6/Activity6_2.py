import datetime
import os
import random
import math

print("--- 1. ทดลองใช้โมดูล datetime (จัดการวันที่และเวลา) ---")
current_time = datetime.datetime.now()
print(f"วันและเวลาปัจจุบัน: {current_time}")

print("\n--- 2. ทดลองใช้โมดูล os (จัดการระบบไฟล์) ---")
current_folder = os.getcwd() 
print(f"ตำแหน่งโฟลเดอร์ปัจจุบัน (Current Directory): {current_folder}")

print("\n--- 3. ทดลองใช้โมดูล random (การสุ่ม) ---")
lucky_number = random.randint(1, 50)
print(f"สุ่มตัวเลขนำโชคระหว่าง 1 ถึง 50: {lucky_number}")

print("\n--- 4. ทดลองใช้โมดูล math (คณิตศาสตร์) ---")
pi_value = math.pi
circle_area = math.pi * (radius := 5) ** 2
print(f"ค่า Pi: {pi_value:.2f}")
print(f"พื้นที่วงกลมรัศมี 5 หน่วย: {circle_area:.2f}")