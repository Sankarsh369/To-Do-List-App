import json
import datetime
import uuid # For generating unique IDs

class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = self._load_tasks()

    def _load_tasks(self):
        try:
            with open(self.filename, 'r') as f:
                loaded_tasks = json.load(f)
                # Ensure all loaded tasks have a 'created_at' and 'id' for backward compatibility
                for task in loaded_tasks:
                    if 'id' not in task:
                        task['id'] = str(uuid.uuid4())
                    if 'created_at' not in task:
                        task['created_at'] = datetime.datetime.now().isoformat()
                    if 'category' not in task: # Add default category
                        task['category'] = 'Uncategorized'
                    if 'due_date' not in task: # Add default due_date
                        task['due_date'] = None
                return loaded_tasks
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            print("Warning: tasks.json is corrupted or empty. Starting with an empty list.")
            return []

    def _save_tasks(self):
        with open(self.filename, 'w') as f:
            json.dump(self.tasks, f, indent=4)

    def add_task(self, description, category='Uncategorized', due_date=None):
        """
        Adds a new task with a unique ID, creation timestamp, category, and optional due date.
        due_date should be in 'YYYY-MM-DD' format if provided.
        """
        if description.strip():
            task_id = str(uuid.uuid4()) # Generate a unique ID for the task
            created_at = datetime.datetime.now().isoformat() # ISO format for easy storage and parsing

            # Validate due_date format if provided
            validated_due_date = None
            if due_date:
                try:
                    # Attempt to parse to ensure it's a valid date
                    datetime.datetime.strptime(due_date, '%Y-%m-%d')
                    validated_due_date = due_date # Keep it as string for storage
                except ValueError:
                    print(f"Warning: Invalid due_date format '{due_date}'. Expected YYYY-MM-DD. Setting due_date to None.")

            self.tasks.append({
                "id": task_id,
                "description": description.strip(),
                "completed": False,
                "created_at": created_at,
                "category": category.strip() if category else 'Uncategorized',
                "due_date": validated_due_date
            })
            self._save_tasks()
            return True
        return False

    def delete_task(self, task_id):
        """Deletes a task by its unique ID."""
        initial_len = len(self.tasks)
        self.tasks = [task for task in self.tasks if task['id'] != task_id]
        if len(self.tasks) < initial_len:
            self._save_tasks()
            return True
        return False

    def toggle_task_status(self, task_id):
        """Toggles the completion status of a task by its unique ID."""
        for task in self.tasks:
            if task['id'] == task_id:
                task["completed"] = not task["completed"]
                self._save_tasks()
                return True
        return False

    def get_tasks(self, category=None, include_completed=True, sort_by='created_at'):
        """
        Returns tasks, optionally filtered by category, and sorted.
        sort_by can be 'created_at', 'due_date', 'description', 'completed'.
        """
        filtered_tasks = []
        for task in self.tasks:
            if category is None or task.get('category') == category:
                if include_completed or not task['completed']:
                    filtered_tasks.append(task)

        # Sorting logic
        if sort_by == 'created_at':
            # Sort by creation date (oldest first)
            filtered_tasks.sort(key=lambda t: datetime.datetime.fromisoformat(t['created_at']))
        elif sort_by == 'due_date':
            # Sort by due date (earliest first), None due dates go to the end
            def sort_key_due_date(task):
                if task.get('due_date'):
                    return datetime.datetime.strptime(task['due_date'], '%Y-%m-%d')
                return datetime.datetime.max # Puts None due dates at the end
            filtered_tasks.sort(key=sort_key_due_date)
        elif sort_by == 'description':
            filtered_tasks.sort(key=lambda t: t['description'].lower())
        elif sort_by == 'completed':
            # Completed tasks at the end
            filtered_tasks.sort(key=lambda t: t['completed'])
        # Add more sorting options as needed

        return filtered_tasks

    def get_categories(self):
        """Returns a list of all unique categories."""
        categories = set()
        for task in self.tasks:
            categories.add(task.get('category', 'Uncategorized'))
        return sorted(list(categories))

# Example Usage (for testing purposes, if run directly)
if __name__ == "__main__":
    task_manager = TaskManager("my_tasks_enhanced.json")

    print("--- Adding Tasks ---")
    task_manager.add_task("Learn Flask for web development", "Programming", "2025-08-15")
    task_manager.add_task("Buy groceries", "Personal", "2025-07-25")
    task_manager.add_task("Prepare presentation", "Work", "2025-07-30")
    task_manager.add_task("Call mom", "Personal")
    task_manager.add_task("Review code", "Programming")
    task_manager.add_task("Write report", "Work", "2025-07-23")
    task_manager.add_task("New uncategorized task")

    print("\n--- All Tasks (Sorted by Creation) ---")
    for task in task_manager.get_tasks():
        print(f"[{'DONE' if task['completed'] else 'TODO'}] "
              f"ID: {task['id'][:8]}... | "
              f"Desc: {task['description']} | "
              f"Category: {task['category']} | "
              f"Due: {task['due_date'] if task['due_date'] else 'N/A'} | "
              f"Created: {task['created_at'].split('T')[0]}")

    print("\n--- Tasks in 'Programming' Category ---")
    for task in task_manager.get_tasks(category="Programming"):
        print(f"[{'DONE' if task['completed'] else 'TODO'}] {task['description']} (Due: {task['due_date']})")

    # Get a task ID to test delete/toggle
    task_to_delete_id = None
    task_to_toggle_id = None
    if task_manager.get_tasks():
        task_to_delete_id = task_manager.get_tasks()[0]['id']
        task_to_toggle_id = task_manager.get_tasks()[1]['id']

    if task_to_toggle_id:
        print(f"\n--- Toggling status for: {task_manager.get_tasks(task_id=task_to_toggle_id)[0]['description']} ---")
        task_manager.toggle_task_status(task_to_toggle_id)
        # Assuming you'd have a way to fetch specific task by ID if needed,
        # but for this example, we just show it after reload.
        print("\n--- All Tasks After Toggle ---")
        for task in task_manager.get_tasks():
            print(f"[{'DONE' if task['completed'] else 'TODO'}] {task['description']} (Category: {task['category']})")


    if task_to_delete_id:
        print(f"\n--- Deleting task with ID: {task_to_delete_id[:8]}... ---")
        task_manager.delete_task(task_to_delete_id)

    print("\n--- All Tasks After Deletion (Sorted by Due Date) ---")
    for task in task_manager.get_tasks(sort_by='due_date'):
        print(f"[{'DONE' if task['completed'] else 'TODO'}] "
              f"Desc: {task['description']} | "
              f"Category: {task['category']} | "
              f"Due: {task['due_date'] if task['due_date'] else 'N/A'}")

    print("\n--- Available Categories ---")
    print(task_manager.get_categories())