#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import sqlite3

SERVER_DIR = 'polls'

if not os.path.exists(SERVER_DIR + '/tasks.sqlite3'):
    
    print("Creating task database")
    conn = sqlite3.connect(SERVER_DIR + '/tasks.sqlite3')
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS TaskList (id INTEGER PRIMARY KEY AUTOINCREMENT, User TEXT NOT NULL, Name TEXT NOT NULL);")
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS Task (id INTEGER PRIMARY KEY AUTOINCREMENT, List INTEGER NOT NULL, TaskName TEXT NOT NULL UNIQUE, Complete INTEGER DEFAULT 0);")
    conn.commit()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'insecureSite.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
