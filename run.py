"""Tiny launcher for the todo CLI for local use.

Run with: python run.py add "Buy milk"
"""
from todo.cli import main


if __name__ == "__main__":
    raise SystemExit(main())