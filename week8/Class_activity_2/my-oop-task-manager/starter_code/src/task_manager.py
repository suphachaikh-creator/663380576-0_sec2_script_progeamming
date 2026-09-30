"""Manage task objects and persist them as JSON."""

import json
import os
from typing import List

try:
    from .task import Task
except ImportError:
    from task import Task


class TaskManager:
    """Add, list, complete, delete, load, and save tasks."""

    def __init__(self, data_file: str = "data/tasks.json"):
        self.data_file = os.fspath(data_file)
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if os.path.isabs(self.data_file):
            self._file_path = self.data_file
        else:
            self._file_path = os.path.abspath(
                os.path.join(project_root, self.data_file)
            )
        self.tasks: List[Task] = self._load_tasks()
        self.next_id = self._get_next_task_id()

    def _get_next_task_id(self) -> int:
        """Return one greater than the largest current task ID."""
        return max((task.id for task in self.tasks), default=0) + 1

    def _load_tasks(self) -> List[Task]:
        """Load JSON tasks and deserialize them into Task instances."""
        try:
            os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
            with open(self._file_path, "r", encoding="utf-8") as file:
                raw_data = json.load(file)

            if not isinstance(raw_data, list):
                raise ValueError("the top-level JSON value must be a list")

            loaded_tasks = []
            seen_ids = set()
            for index, item in enumerate(raw_data, start=1):
                if not isinstance(item, dict):
                    raise ValueError(f"task #{index} must be a JSON object")

                task_id = item.get("id")
                description = item.get("description")
                completed = item.get("completed", False)
                if (
                    isinstance(task_id, bool)
                    or not isinstance(task_id, int)
                    or task_id <= 0
                ):
                    raise ValueError(f"task #{index} must have a positive integer ID")
                if task_id in seen_ids:
                    raise ValueError(f"duplicate task ID {task_id}")
                if not isinstance(description, str) or not description.strip():
                    raise ValueError(f"task #{index} must have a non-empty description")
                if not isinstance(completed, bool):
                    raise ValueError(f"task #{index} completed must be true or false")

                loaded_tasks.append(Task(task_id, description.strip(), completed))
                seen_ids.add(task_id)
            return loaded_tasks

        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, ValueError, TypeError) as error:
            print(
                "Warning: tasks.json is invalid or corrupted "
                f"({error}). Starting with an empty task list."
            )
            return []
        except OSError as error:
            print(f"Error: Could not read tasks from '{self._file_path}': {error}")
            return []

    def _save_tasks(self) -> bool:
        """Serialize tasks and save them to the configured JSON file."""
        try:
            os.makedirs(os.path.dirname(self._file_path), exist_ok=True)
            with open(self._file_path, "w", encoding="utf-8") as file:
                json.dump(
                    [task.to_dict() for task in self.tasks],
                    file,
                    indent=4,
                    ensure_ascii=False,
                )
            return True
        except OSError as error:
            print(f"Error: Could not save tasks to '{self._file_path}': {error}")
            return False

    def add_task(self, description: str) -> Task:
        """Create, store, and persist a new task."""
        if not isinstance(description, str) or not description.strip():
            raise ValueError("Task description cannot be empty.")

        new_task = Task(self.next_id, description.strip())
        self.tasks.append(new_task)
        self.next_id += 1
        if self._save_tasks():
            print(f"Task '{new_task.description}' added with ID {new_task.id}.")
        return new_task

    def list_tasks(self) -> None:
        """Print all tasks, or a message when there are none."""
        if not self.tasks:
            print("No tasks found.")
            return
        for task in self.tasks:
            print(task)

    def complete_task(self, task_id: int) -> bool:
        """Mark a matching task completed and persist the change."""
        for task in self.tasks:
            if task.id == task_id:
                if task.completed:
                    print(f"Task ID {task_id} is already completed.")
                    return True
                task.mark_complete()
                if self._save_tasks():
                    print(f"Task ID {task_id} marked as completed.")
                return True

        print(f"Error: Task with ID {task_id} not found.")
        return False

    def delete_task(self, task_id: int) -> bool:
        """Delete a matching task and persist the change."""
        remaining_tasks = [task for task in self.tasks if task.id != task_id]
        if len(remaining_tasks) == len(self.tasks):
            print(f"Error: Task with ID {task_id} not found.")
            return False

        self.tasks = remaining_tasks
        if self._save_tasks():
            print(f"Task ID {task_id} deleted successfully.")
        return True
