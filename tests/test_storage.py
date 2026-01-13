import json
from todo.storage import TodoStorage


def test_add_and_list(tmp_path):
    p = tmp_path / "t.json"
    storage = TodoStorage(path=str(p))
    assert storage.list() == []
    tid = storage.add("write tests")
    todos = storage.list()
    assert any(t["id"] == tid and t["text"] == "write tests" for t in todos)


def test_complete_and_remove(tmp_path):
    p = tmp_path / "t2.json"
    storage = TodoStorage(path=str(p))
    tid = storage.add("task")
    assert storage.complete(tid) is True
    todos = storage.list()
    assert any(t["id"] == tid and t["done"] for t in todos)
    assert storage.remove(tid) is True
    assert storage.list() == []


def test_edit_and_filters(tmp_path):
    p = tmp_path / "t3.json"
    storage = TodoStorage(path=str(p))
    t1 = storage.add("pay bills", priority=1, due="2026-01-20")
    t2 = storage.add("buy milk", priority=2, due="2026-02-01")
    # edit text and priority
    assert storage.edit(t2, text="buy almond milk", priority=1)
    all_todos = storage.list(show_all=True)
    assert any(t["id"] == t2 and "almond" in t["text"] for t in all_todos)
    # filter by priority
    p1 = storage.list(show_all=True, priority=1)
    assert len(p1) >= 2
    # due_before filter
    due_early = storage.list(show_all=True, due_before="2026-01-25")
    assert any(t["id"] == t1 for t in due_early)
