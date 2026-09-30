# src/task_manager.py
"""
โมดูล task_manager.py: Business Logic Layer ของระบบ Enhanced Task Manager
ทำหน้าที่จัดการ collection ของ Task objects, ควบคุมการทำงาน CRUD,
และเป็นพื้นที่ให้นักศึกษาพัฒนาตรรกะสำหรับการค้นหา (Search), การกรอง (Filter), และการจัดเรียง (Sort)
"""

import datetime
try:
    from .task import Task, DueDateTask, PriorityTask
    from .data_persistence import DataPersistence
except ImportError:
    from task import Task, DueDateTask, PriorityTask
    from data_persistence import DataPersistence



class TaskManager:
    """
    คลาสจัดการงาน (Task Manager)
    มุ่งเน้นที่ Business Logic ล้วนๆ ไม่มีการเข้าถึงไฟล์ I/O หรือ CLI Input/Output โดยตรง
    ตามหลักการ Separation of Concerns
    """
    def __init__(self, data_file='data/tasks.json'):
        self.persistence = DataPersistence(data_file)
        self.tasks = self.persistence.load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self):
        """คำนวณหา ID ลำดับถัดไปที่ไม่ซ้ำกันสำหรับงานใหม่"""
        if not self.tasks:
            return 1
        return max(task.id for task in self.tasks) + 1

    def _save_changes(self):
        """บันทึกข้อมูลการเปลี่ยนแปลงไปยัง Data Persistence Layer"""
        self.persistence.save_tasks(self.tasks)

    # =========================================================================
    # การดำเนินการ CRUD พื้นฐาน (พร้อมใช้งาน)
    # =========================================================================

    def add_normal_task(self, description, tags=None):
        """เพิ่มงานทั่วไป (Normal Task)"""
        new_task = Task(self.next_id, description, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def add_due_date_task(self, description, due_date_str, tags=None):
        """เพิ่มงานที่มีวันครบกำหนด (Due Date Task)"""
        new_task = DueDateTask(self.next_id, description, due_date_str, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def add_priority_task(self, description, priority, tags=None):
        """เพิ่มงานที่มีระดับความสำคัญ (Priority Task)"""
        new_task = PriorityTask(self.next_id, description, priority, tags=tags)
        self.tasks.append(new_task)
        self.next_id += 1
        self._save_changes()
        return new_task

    def get_task_by_id(self, task_id):
        """ค้นหางานตาม ID"""
        return next((task for task in self.tasks if task.id == task_id), None)

    def complete_task(self, task_id):
        """ทำเครื่องหมายว่างานเสร็จสมบูรณ์แล้ว"""
        task = self.get_task_by_id(task_id)
        if task:
            if not task.completed:
                task.mark_complete()
                self._save_changes()
                return True, f"งาน ID {task_id} ถูกเปลี่ยนสถานะเป็น 'เสร็จสมบูรณ์ (Completed)' แล้ว"
            else:
                return False, f"งาน ID {task_id} มีสถานะเสร็จสมบูรณ์อยู่แล้ว"
        return False, f"ไม่พบงาน ID {task_id} ในระบบ"

    def delete_task(self, task_id):
        """ลบงานออกจากระบบตาม ID"""
        original_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task.id != task_id]
        if len(self.tasks) < original_len:
            self._save_changes()
            return True, f"ลบงาน ID {task_id} เรียบร้อยแล้ว"
        return False, f"ไม่พบงาน ID {task_id} ในระบบ"

    def get_all_tasks(self):
        """ส่งคืนรายการงานทั้งหมด"""
        return list(self.tasks)

    # =========================================================================
    # ฟังก์ชันเพิ่มเติมสำหรับนักศึกษาพัฒนาต่อ (Student Assignment Placeholders)
    # =========================================================================

    def search_tasks(self, keyword):
        """ค้นหา keyword ในคำอธิบายหรือ tags โดยไม่สนตัวพิมพ์เล็ก/ใหญ่."""
        if not isinstance(keyword, str):
            raise TypeError("keyword must be a string")
        normalized_keyword = keyword.strip().casefold()
        if not normalized_keyword:
            return []
        return [
            task for task in self.tasks
            if normalized_keyword in task.description.casefold()
            or any(normalized_keyword in tag.casefold() for tag in task.tags)
        ]

    def filter_tasks(self, status=None, due_date_before=None, priority=None, tags=None):
        """กรองงานตามเงื่อนไขที่กำหนด โดยรวมหลายเงื่อนไขด้วย AND."""
        filtered = list(self.tasks)
        if status is not None:
            if not isinstance(status, bool):
                raise TypeError("status must be True, False, or None")
            filtered = [task for task in filtered if task.completed is status]

        if due_date_before is not None:
            if isinstance(due_date_before, datetime.datetime):
                cutoff_date = due_date_before.date()
            elif isinstance(due_date_before, datetime.date):
                cutoff_date = due_date_before
            elif isinstance(due_date_before, str):
                try:
                    cutoff_date = datetime.datetime.strptime(due_date_before.strip(), "%Y-%m-%d").date()
                except ValueError as error:
                    raise ValueError("due_date_before must use YYYY-MM-DD format") from error
            else:
                raise TypeError("due_date_before must be a date or YYYY-MM-DD string")
            filtered = [
                task for task in filtered
                if isinstance(task, DueDateTask) and task.due_date <= cutoff_date
            ]

        if priority is not None:
            if not isinstance(priority, str) or not priority.strip():
                raise ValueError("priority must be High, Medium, or Low")
            normalized_priority = priority.strip().casefold()
            if normalized_priority not in {"high", "medium", "low"}:
                raise ValueError("priority must be High, Medium, or Low")
            filtered = [
                task for task in filtered
                if isinstance(task, PriorityTask)
                and task.priority.casefold() == normalized_priority
            ]

        if tags is not None:
            if isinstance(tags, str):
                requested_tags = {tags.strip().casefold()} if tags.strip() else set()
            else:
                try:
                    requested_tags = {
                        tag.strip().casefold() for tag in tags
                        if isinstance(tag, str) and tag.strip()
                    }
                except TypeError as error:
                    raise TypeError("tags must be a string or an iterable of strings") from error
            if not requested_tags:
                return []
            filtered = [
                task for task in filtered
                if requested_tags.intersection(tag.casefold() for tag in task.tags)
            ]
        return filtered

    def sort_tasks(self, criterion="id", reverse=False):
        """เรียงงานตาม id, due_date หรือ priority โดยไม่แก้ลำดับเดิมใน manager."""
        if not isinstance(criterion, str):
            raise TypeError("criterion must be a string")
        criterion = criterion.strip().casefold()
        if criterion == "id":
            return sorted(self.tasks, key=lambda task: task.id, reverse=reverse)
        if criterion == "due_date":
            dated_tasks = sorted(
                (task for task in self.tasks if isinstance(task, DueDateTask)),
                key=lambda task: task.due_date,
                reverse=reverse,
            )
            undated_tasks = sorted(
                (task for task in self.tasks if not isinstance(task, DueDateTask)),
                key=lambda task: task.id,
            )
            return dated_tasks + undated_tasks
        if criterion == "priority":
            priority_order = {"high": 0, "medium": 1, "low": 2}
            priority_tasks = sorted(
                (task for task in self.tasks if isinstance(task, PriorityTask)),
                key=lambda task: (priority_order.get(task.priority.casefold(), 3), task.id),
                reverse=reverse,
            )
            other_tasks = sorted(
                (task for task in self.tasks if not isinstance(task, PriorityTask)),
                key=lambda task: task.id,
            )
            return priority_tasks + other_tasks
        raise ValueError("criterion must be one of: id, due_date, priority")
