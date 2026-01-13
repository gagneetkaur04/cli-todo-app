import argparse
import sys
from .storage import TodoStorage


def _print_todo(t: dict) -> None:
    status = "x" if t.get("done") else " "
    parts = [f"[{status}] {t.get('id')}: {t.get('text')}"]
    pr = t.get("priority")
    if pr is not None:
        parts.append(f"prio={pr}")
    due = t.get("due")
    if due:
        parts.append(f"due={due}")
    print(" ".join(parts))


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(prog="todo", description="Simple CLI todo manager")
    subparsers = parser.add_subparsers(dest="command")

    p_add = subparsers.add_parser("add", help="Add a new todo")
    p_add.add_argument("text", nargs="+", help="Text for the todo")
    p_add.add_argument("--priority", type=int, help="Priority (lower = higher priority)")
    p_add.add_argument("--due", help="Due date (YYYY-MM-DD)")

    p_list = subparsers.add_parser("list", help="List todos")
    p_list.add_argument("--all", action="store_true", help="Show all todos (including done)")
    p_list.add_argument("--priority", type=int, help="Filter by priority")
    p_list.add_argument("--due-before", help="Show todos due on or before this date (YYYY-MM-DD)")
    p_list.add_argument("--query", help="Filter todos by text substring")

    p_done = subparsers.add_parser("done", help="Mark todo as done")
    p_done.add_argument("id", type=int, help="ID of todo to mark done")

    p_remove = subparsers.add_parser("remove", help="Remove a todo")
    p_remove.add_argument("id", type=int, help="ID of todo to remove")

    p_edit = subparsers.add_parser("edit", help="Edit a todo")
    p_edit.add_argument("id", type=int, help="ID of todo to edit")
    p_edit.add_argument("--text", nargs="+", help="New text for the todo")
    p_edit.add_argument("--priority", type=int, help="New priority")
    p_edit.add_argument("--due", help="New due date (YYYY-MM-DD) or empty to clear")

    p_find = subparsers.add_parser("find", help="Find todos by text")
    p_find.add_argument("query", nargs="+", help="Search query string")

    args = parser.parse_args(argv)
    storage = TodoStorage()

    if args.command == "add":
        text = " ".join(args.text)
        todo_id = storage.add(text, priority=args.priority, due=args.due)
        print(f"Added todo {todo_id}")
        return 0

    if args.command == "list":
        todos = storage.list(show_all=args.all, query=args.query, priority=args.priority, due_before=args.due_before)
        if not todos:
            print("No todos.")
            return 0
        for t in todos:
            _print_todo(t)
        return 0

    if args.command == "done":
        ok = storage.complete(args.id)
        if ok:
            print(f"Marked {args.id} done")
            return 0
        print(f"Todo {args.id} not found")
        return 2

    if args.command == "remove":
        ok = storage.remove(args.id)
        if ok:
            print(f"Removed {args.id}")
            return 0
        print(f"Todo {args.id} not found")
        return 2

    if args.command == "edit":
        text = None
        if args.text:
            text = " ".join(args.text)
        due = args.due
        if due == "":
            due = None
        ok = storage.edit(args.id, text=text, priority=args.priority, due=due)
        if ok:
            print(f"Edited {args.id}")
            return 0
        print(f"Todo {args.id} not found")
        return 2

    if args.command == "find":
        query = " ".join(args.query)
        todos = storage.list(show_all=True, query=query)
        if not todos:
            print("No todos found.")
            return 0
        for t in todos:
            _print_todo(t)
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
