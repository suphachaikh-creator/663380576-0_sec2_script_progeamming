
def greet(name):
    print(f"Hello, {name}!")

def is_prime(number):
    """
    ฟังก์ชันตรวจสอบว่าตัวเลขที่รับเข้ามาเป็นจำนวนเฉพาะหรือไม่คืนค่า True หากเป็นจำนวนเฉพาะ, False หากไม่ใช่
    """
    if number <= 1:
        return False
    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False
    return True