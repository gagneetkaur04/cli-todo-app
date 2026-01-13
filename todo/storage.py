import json
from typing import List, Dict, Optional
from datetime import datetime


class TodoStorage:
    """JSON-backed storage for todos with priority and due-date support."""

    def __init__(self, path: str = "todos.json"):
        self.path = path
        self._data: Dict[str, List[Dict]] = {"todos": []}
        self.load()

    def load(self) -> None:
        try:
            with open(self.path, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except FileNotFoundError:
            self._data = {"todos": []}
            self.save()
        except json.JSONDecodeError:
            self._data = {"todos": []}
            self.save()

    def save(self) -> None:
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(self._data, f, indent=2, ensure_ascii=False)

    def _next_id(self) -> int:
        todos = self._data.get("todos", [])
        if not todos:
            return 1
        return max(t["id"] for t in todos) + 1

    def add(self, text: str, priority: Optional[int] = None, due: Optional[str] = None) -> int:
        """Add a new todo. `priority` is an int (lower is higher priority).
        `due` should be an ISO date string (YYYY-MM-DD) or None."""
        todo = {
            "id": self._next_id(),
            "text": text,
            "done": False,
            "priority": priority,
            "due": due,
        }
        self._data.setdefault("todos", []).append(todo)
        self.save()
        return todo["id"]

    def edit(self, todo_id: int, text: Optional[str] = None, priority: Optional[int] = None, due: Optional[str] = None) -> bool:
        for t in self._data.get("todos", []):
            if t.get("id") == todo_id:
                if text is not None:
                    t["text"] = text
                if priority is not None:
                    t["priority"] = priority
                if due is not None:
                    t["due"] = due
                self.save()
                return True
        return False

    def list(self, show_all: bool = True, query: Optional[str] = None, priority: Optional[int] = None, due_before: Optional[str] = None) -> List[Dict]:
        todos = list(self._data.get("todos", []))
        if query:
            todos = [t for t in todos if query.lower() in t.get("text", "").lower()]
        if priority is not None:
            todos = [t for t in todos if t.get("priority") == priority]
        if due_before is not None:
            try:
                cutoff = datetime.fromisoformat(due_before)
                def parse_due(s: Optional[str]):
                    if not s:
                        return None
                    try:
                        return datetime.fromisoformat(s)
                    except Exception:
                        return None
                todos = [t for t in todos if (d := parse_due(t.get("due"))) is not None and d <= cutoff]
            except Exception:
                pass
        if show_all:
            return todos
        return [t for t in todos if not t.get("done")]

    def complete(self, todo_id: int) -> bool:
        for t in self._data.get("todos", []):
            if t.get("id") == todo_id:
                t["done"] = True
                self.save()
                return True
        return False

    def remove(self, todo_id: int) -> bool:
        todos = self._data.get("todos", [])
        for i, t in enumerate(todos):
            if t.get("id") == todo_id:
                todos.pop(i)
                self.save()
                return True
        return False


__all__ = ["TodoStorage"]
