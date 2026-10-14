"""Represent one task and its state."""


class Task:
    """A single task in the task manager."""

    def __init__(self, id: int, description: str, completed: bool = False):
        """Create a task with an ID, description, and completion state."""
        self.id = id
        self.description = description
        self.completed = completed

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True

    def to_dict(self) -> dict:
        """Return a JSON-serializable representation of the task."""
        return {
            "id": self.id,
            "description": self.description,
            "completed": self.completed,
        }

    def __str__(self) -> str:
        """Return a user-friendly task description."""
        status = "Completed" if self.completed else "Pending"
        return f"ID: {self.id} | Description: {self.description} | Status: {status}"

    def __repr__(self) -> str:
        """Return an unambiguous representation for debugging."""
        return (
            f"Task(id={self.id}, description={self.description!r}, "
            f"completed={self.completed})"
        )
