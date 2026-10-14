"""Interactive CLI for fetching and exporting JSONPlaceholder API data."""

import json
import os
import sys
from typing import Any, Optional

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, OSError):
        pass

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
from api_client import APIClient


def display_menu() -> None:
    print("\n" + "=" * 52)
    print("   Web API Data Fetcher CLI (Week 10)")
    print("=" * 52)
    print("  1. ดึงข้อมูลงานเดี่ยว (Single TODO)")
    print("  2. ดึงรายการโพสต์ทั้งหมด (All Posts)")
    print("  3. ดึงรายการ TODO ตาม User ID")
    print("  4. ดึงข้อมูลโปรไฟล์ผู้ใช้ (User Profile)")
    print("  5. ดึงคอมเมนต์ของโพสต์ (Post Comments)")
    print("  6. ดึงข้อมูลแล้วบันทึกเป็นไฟล์ JSON (Fetch & Export)")
    print("  7. ออกจากโปรแกรม (Exit)")
    print("=" * 52)


def read_positive_int(prompt: str) -> Optional[int]:
    raw = input(prompt).strip()
    try:
        value = int(raw)
    except ValueError:
        print("❌ กรุณาป้อนตัวเลขจำนวนเต็มเท่านั้น")
        return None
    if value <= 0:
        print("❌ กรุณาป้อนตัวเลขจำนวนเต็มที่มากกว่า 0")
        return None
    return value


def handle_single_todo(client: APIClient) -> None:
    todo_id = read_positive_int("ป้อน TODO ID: ")
    if todo_id is None:
        return
    todo = client.fetch_single_todo(todo_id)
    if not todo:
        print(f"⚠️ ไม่พบ TODO ID {todo_id} หรือเรียก API ไม่สำเร็จ")
        return
    status = "เสร็จแล้ว ✅" if todo.get("completed") else "ยังไม่เสร็จ ⏳"
    print(f"\nTODO #{todo.get('id')} | User #{todo.get('userId')}\nหัวข้อ: {todo.get('title')}\nสถานะ: {status}")


def handle_all_posts(client: APIClient) -> None:
    posts = client.fetch_all_posts()
    if posts is None:
        print("⚠️ ไม่สามารถดึงรายการโพสต์ได้")
        return
    print(f"\nพบโพสต์ทั้งหมด {len(posts)} รายการ; แสดง 5 รายการแรก")
    for post in posts[:5]:
        print(f"\nPost #{post.get('id')} | User #{post.get('userId')}\nหัวข้อ: {post.get('title')}\n{post.get('body', '')}")


def handle_user_todos(client: APIClient) -> None:
    user_id = read_positive_int("ป้อน User ID: ")
    if user_id is None:
        return
    todos = client.fetch_user_todos(user_id)
    if todos is None:
        print("⚠️ ไม่สามารถดึงรายการ TODO ได้")
        return
    print(f"\nพบ TODO ของ User #{user_id} จำนวน {len(todos)} รายการ")
    for todo in todos:
        icon = "✅" if todo.get("completed") else "⏳"
        print(f"{icon} [{todo.get('id')}] {todo.get('title')}")


def handle_user_profile(client: APIClient) -> None:
    user_id = read_positive_int("ป้อน User ID: ")
    if user_id is None:
        return
    user = client.fetch_user_profile(user_id)
    if not user:
        print(f"⚠️ ไม่พบโปรไฟล์ User ID {user_id} หรือเรียก API ไม่สำเร็จ")
        return
    company = user.get("company") or {}
    address = user.get("address") or {}
    print(f"\nโปรไฟล์ผู้ใช้ #{user.get('id')}")
    print(f"ชื่อ: {user.get('name', 'ไม่ระบุ')}")
    print(f"Username: {user.get('username', 'ไม่ระบุ')}")
    print(f"อีเมล: {user.get('email', 'ไม่ระบุ')}")
    print(f"โทรศัพท์: {user.get('phone', 'ไม่ระบุ')}")
    print(f"บริษัท: {company.get('name', 'ไม่ระบุ')}")
    print(f"เมือง: {address.get('city', 'ไม่ระบุ')}")


def handle_post_comments(client: APIClient) -> None:
    post_id = read_positive_int("ป้อน Post ID: ")
    if post_id is None:
        return
    comments = client.fetch_post_comments(post_id)
    if comments is None:
        print("⚠️ ไม่สามารถดึงคอมเมนต์ได้")
        return
    print(f"\nพบคอมเมนต์ทั้งหมด {len(comments)} รายการ; แสดงไม่เกิน 3 รายการแรก")
    for index, comment in enumerate(comments[:3], 1):
        print(f"\n[{index}] {comment.get('name', 'ไม่ระบุชื่อ')} <{comment.get('email', 'ไม่ระบุอีเมล')}>")
        print(comment.get("body", ""))


def export_to_json_file(filename: str, data: Any) -> bool:
    """บันทึกข้อมูล JSON เป็น UTF-8 พร้อมจัดรูปแบบให้อ่านง่าย"""
    try:
        with open(filename, "w", encoding="utf-8") as output_file:
            json.dump(data, output_file, indent=4, ensure_ascii=False)
        print(f"✅ บันทึกไฟล์สำเร็จ: {filename}")
        return True
    except (OSError, TypeError, ValueError) as error:
        print(f"❌ บันทึกไฟล์ไม่สำเร็จ: {error}")
        return False


def handle_fetch_export(client: APIClient) -> None:
    print("\nเลือกข้อมูลที่จะดึงและบันทึก: 1) TODO  2) User Profile  3) Post Comments")
    kind = input("เลือก (1-3): ").strip()
    if kind not in {"1", "2", "3"}:
        print("⚠️ ตัวเลือกไม่ถูกต้อง")
        return
    label = {"1": "TODO ID", "2": "User ID", "3": "Post ID"}[kind]
    record_id = read_positive_int(f"ป้อน {label}: ")
    if record_id is None:
        return

    if kind == "1":
        data = client.fetch_single_todo(record_id)
        default_name = f"todo_{record_id}.json"
    elif kind == "2":
        data = client.fetch_user_profile(record_id)
        default_name = f"user_{record_id}_profile.json"
    else:
        data = client.fetch_post_comments(record_id)
        default_name = f"post_{record_id}_comments.json"
    if data is None:
        print("⚠️ ไม่มีข้อมูลให้บันทึก")
        return

    filename = input(f"ชื่อไฟล์ (Enter เพื่อใช้ {default_name}): ").strip() or default_name
    export_to_json_file(filename, data)


def main() -> None:
    client = APIClient()
    actions = {
        "1": handle_single_todo,
        "2": handle_all_posts,
        "3": handle_user_todos,
        "4": handle_user_profile,
        "5": handle_post_comments,
        "6": handle_fetch_export,
    }
    while True:
        display_menu()
        choice = input("เลือกเมนู (1-7): ").strip()
        if choice == "7":
            print("👋 ขอบคุณที่ใช้งานโปรแกรม")
            break
        action = actions.get(choice)
        if action is None:
            print("⚠️ ตัวเลือกไม่ถูกต้อง กรุณาเลือก 1 ถึง 7")
            continue
        action(client)


if __name__ == "__main__":
    main()
