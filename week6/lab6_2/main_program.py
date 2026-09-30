import my_utils
import math
import random

print("--- ทดสอบการใช้งาน Custom Module (my_utils) ---")

# เรียกใช้ฟังก์ชัน greet จาก my_utils
my_utils.greet("Alice")

test_numbers = [7, 10, 13, 1]
for num in test_numbers:
    result = my_utils.is_prime(num)
    print(f"เลข {num} เป็นจำนวนเฉพาะหรือไม่? -> {result}")
    
print("\n--- ทดสอบการใช้งาน Standard Library (math, random) ---")

# ใช้ math.sqrt() เพื่อคำนวณหารากที่สองของตัวเลข
number_to_sqrt = 25
square_root_result = math.sqrt(number_to_sqrt)
print(f"รากที่สองของ {number_to_sqrt} คือ: {square_root_result}")

# ใช้ random.randint() เพื่อสุ่มตัวเลขระหว่าง 1 ถึง 100
random_num = random.randint(1, 100)
print(f"สุ่มตัวเลขระหว่าง 1 ถึง 100 ได้: {random_num}")