# CLI To‑Do Manager (Minimal)

This is a small Python CLI to-do manager used for the MLH Copilot challenge.

Quick start

```bash
python run.py add "Buy groceries"
python run.py list
python run.py done 1
python run.py remove 1
```

Notes

- Todos are stored in `todos.json` in the current working directory.
- Tests are in `tests/` and require `pytest`.

New features

- Add a todo with `--priority` and `--due`:

```bash
python run.py add "Finish project" --priority 1 --due 2026-01-20
```

- Edit a todo:

```bash
python run.py edit 2 --text "Buy almond milk" --priority 1
```

- Find todos by text:

```bash
python run.py find milk
```

- List filtered by priority or due date:

```bash
python run.py list --priority 1
python run.py list --due-before 2026-01-25
```
