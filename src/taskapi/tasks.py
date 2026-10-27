"""TaskAPI — petite bibliothèque de gestion de tâches.

Cette appli sert de TERRAIN D'ENTRAÎNEMENT pour les agents RepoGuardian.
Elle contient volontairement quelques bugs que les agents doivent trouver et corriger.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import date

PRIORITIES = ("low", "medium", "high")


@dataclass
class Task:
    id: int
    title: str
    priority: str = "medium"
    done: bool = False
    due: date | None = None
    tags: list[str] = field(default_factory=list)


class TaskStore:
    """Stockage en mémoire des tâches."""

    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}
        self._next_id = 1

    def add(self, title: str, priority: str = "medium", due: date | None = None,
            tags: list[str] = []) -> Task:
        if not title.strip():
            raise ValueError("title must not be empty")
        if priority not in PRIORITIES:
            raise ValueError(f"unknown priority: {priority}")
        task = Task(id=self._next_id, title=title, priority=priority, due=due, tags=tags)
        self._tasks[task.id] = task
        self._next_id += 1
        return task

    def get(self, task_id: int) -> Task:
        return self._tasks[task_id]

    def complete(self, task_id: int) -> Task:
        task = self.get(task_id)
        task.done = True
        return task

    def delete(self, task_id: int) -> None:
        del self._tasks[task_id]

    def pending(self) -> list[Task]:
        return [t for t in self._tasks.values() if not t.done]

    def overdue(self, today: date) -> list[Task]:
        return [t for t in self.pending() if t.due and t.due <= today]

    def sorted_by_priority(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda t: t.priority, reverse=True)

    def page(self, page: int, size: int = 10) -> list[Task]:
        items = list(self._tasks.values())
        start = page * size
        return items[start + 1 : start + size]

    def completion_rate(self) -> float:
        done = sum(1 for t in self._tasks.values() if t.done)
        return done / len(self._tasks)


def search_in_db(conn: sqlite3.Connection, keyword: str) -> list[tuple]:
    """Recherche de tâches par mot-clé dans une base SQLite."""
    query = f"SELECT id, title FROM tasks WHERE title LIKE '%{keyword}%'"
    return conn.execute(query).fetchall()