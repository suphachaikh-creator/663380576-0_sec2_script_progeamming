"""Command-line interface for the OOP task manager."""

import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
SRC_DIR = PROJECT_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from task_manager import TaskManager


def display_menu() -> None:
    """Display the available task manager commands."""
    print("\n==============================")
    print("   OOP TASK MANAGER CLI")
    print("==============================")
    print("1. Add Task")
    print("2. List Tasks")
    print("3. Complete Task")
    print("4. Delete Task")
    print("5. Exit")
    print("------------------------------")


def read_task_id(prompt: str) -> int:
    """Read and validate a positive task ID from the user."""
    raw_value = input(prompt).strip().lstrip("#")
    task_id = int(raw_value)
    if task_id <= 0:
        raise ValueError("Task ID must be a positive number.")
    return task_id


def main() -> None:
    """Run the interactive task manager until the user exits."""
    manager = TaskManager()
    try:
        while True:
            display_menu()
            choice = input("Enter your choice (1-5): ").strip()

            if choice == "1":
                description = input("Enter task description: ").strip()
                if not description:
                    print("Task description cannot be empty.")
                    continue
                try:
                    manager.add_task(description)
                except ValueError as error:
                    print(f"Invalid task: {error}")
            elif choice == "2":
                manager.list_tasks()
            elif choice == "3":
                try:
                    task_id = read_task_id("Enter ID of task to complete: ")
                    manager.complete_task(task_id)
                except ValueError:
                    print("Invalid input. Enter a positive whole number for the task ID.")
            elif choice == "4":
                try:
                    task_id = read_task_id("Enter ID of task to delete: ")
                    manager.delete_task(task_id)
                except ValueError:
                    print("Invalid input. Enter a positive whole number for the task ID.")
            elif choice == "5":
                print("Exiting Task Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please select an option from 1 to 5.")
    except (KeyboardInterrupt, EOFError):
        print("\nInput interrupted. Your latest changes are already saved. Goodbye!")


if __name__ == "__main__":
    main()
