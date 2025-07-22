# To-Do List App (Desktop)

A feature-rich desktop To-Do List application built with Python and Tkinter, offering advanced task management capabilities including categories, due dates, filtering, and sorting.

---

## Features

* **Add Tasks:** Quickly add new tasks with a description, an optional category (like 'Work', 'Personal'), and an optional due date.
* **Unique Task IDs:** Each task is assigned a unique identifier for reliable management.
* **Creation Timestamps:** Automatically records when each task was created.
* **Categorization:** Organize your tasks into custom categories/folders.
* **Due Dates:** Assign deadlines to your tasks. Overdue tasks are visually highlighted.
* **Toggle Status:** Mark tasks as completed or incomplete. Completed tasks are visually distinct.
* **Delete Tasks:** Remove unwanted tasks from your list.
* **Filter by Category:** View tasks specific to a chosen category, or see 'All' tasks.
* **Sort Tasks:** Order your tasks by Creation Date, Due Date, Description, or Status.
* **Show/Hide Completed:** Easily toggle the visibility of completed tasks.
* **Data Persistence:** All tasks are automatically saved to a `tasks.json` file, so your data is retained between sessions.
* **Modern UI:** Utilizes `tkinter.ttk` for a cleaner, more contemporary look.

---

## Project Structure
odo_app_desktop/
├── main.py             # Main entry point of the application
├── gui.py              # Handles the Graphical User Interface (Tkinter)
├── task_manager.py     # Manages all task data logic (add, delete, update, retrieve)
└── styles.py           # Centralized styling configurations for Tkinter widgets
---

## Setup and Installation

To run this To-Do List application, follow these steps:

1.  **Clone or Download the Project:**
    If you're using Git:
    ```bash
    git clone <repository_url>
    cd todo_app_desktop
    ```
    Alternatively, download the project as a ZIP file and extract it. Navigate into the `todo_app_desktop` folder.

2.  **Ensure Python is Installed:**
    This application requires **Python 3.x**. If you don't have it, download and install it from [python.org](https://www.python.org/downloads/).

3.  **No External Libraries Needed for Tkinter:**
    Tkinter is usually included with standard Python installations, so you typically don't need to install it separately.

4.  **Place the Files:**
    Make sure all the `.py` files (`main.py`, `gui.py`, `task_manager.py`, `styles.py`) are placed in the same directory (e.g., `todo_app_desktop`).

---

## How to Run the Application

1.  **Open your Terminal or Command Prompt.**
2.  **Navigate to the project directory:**
    ```bash
    cd path/to/your/todo_app_desktop
    ```
    (Replace `path/to/your/todo_app_desktop` with the actual path where you saved the files).
3.  **Run the main script:**
    ```bash
    python main.py
    ```

The To-Do List application window should now appear on your desktop.

---

## Usage

* **Adding a Task:**
    * Enter the task description in the "Description" field.
    * Optionally, type a category in the "Category" field (e.g., "Work", "Personal").
    * Optionally, enter a due date in `YYYY-MM-DD` format in the "Due Date" field.
    * Click the **"Add Task"** button or press **Enter** in the Description field.
* **Managing Tasks:**
    * **Select a task** by clicking on it in the list.
    * Click **"Toggle Status"** to mark a task as completed or incomplete. Completed tasks will appear grayed out.
    * Click **"Delete Selected"** to remove the chosen task from the list. A confirmation dialog will appear.
* **Filtering Tasks:**
    * Use the **"Filter Category"** dropdown to view tasks belonging to specific categories, or select "All" to see all tasks.
* **Sorting Tasks:**
    * Use the **"Sort By"** dropdown to reorder your task list based on creation date, due date, description (alphabetically), or completion status.
* **Show/Hide Completed Tasks:**
    * Check or uncheck the **"Show Completed"** box to toggle the visibility of completed tasks in the list.

---

## Data Storage

Your tasks are stored in a file named `tasks.json` located in the same directory as `main.py`. Please do not manually edit this file unless you are familiar with JSON structure, as improper modifications could corrupt your task data.

---

## Contributing

Feel free to fork this repository, suggest improvements, or submit pull requests.

---

## License

This project is open-source and available under the MIT License. (You can specify your preferred license here).
