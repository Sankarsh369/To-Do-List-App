# main.py
import tkinter as tk
import os
from task_manager import TaskManager
from gui import TodoAppGUI

if __name__ == "__main__":
    root = tk.Tk()

    # Ensure tasks.json is in the same directory as app.py
    basedir = os.path.abspath(os.path.dirname(__file__))
    tasks_file_path = os.path.join(basedir, "tasks.json")

    task_manager = TaskManager(filename=tasks_file_path)
    app = TodoAppGUI(root, task_manager)
    root.mainloop()