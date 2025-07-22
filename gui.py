import tkinter as tk
from tkinter import messagebox, ttk
import datetime # To check for overdue tasks
from task_manager import TaskManager
from styles import AppStyles # Import our styles

class TodoAppGUI:
    def __init__(self, master, task_manager):
        self.master = master
        self.master.title("Super To-Do List (Desktop)")
        self.master.geometry("550x750") # Increased size
        self.master.resizable(False, False)
        self.master.config(bg=AppStyles.BG_COLOR)

        self.task_manager = task_manager

        self._configure_styles()
        self._create_widgets()
        self._layout_widgets()
        self._load_tasks_to_listbox() # Initial load

    def _configure_styles(self):
        s = ttk.Style()
        s.theme_use('clam') # 'clam', 'alt', 'default', 'vista', 'xpnative' - 'clam' is often good base

        # General frame style
        s.configure(AppStyles.TTK_FRAME_STYLE, background=AppStyles.BG_COLOR)

        # Entry style
        s.configure(AppStyles.TTK_ENTRY_STYLE,
                    fieldbackground=AppStyles.CARD_BG_COLOR,
                    foreground=AppStyles.TEXT_COLOR,
                    font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_MEDIUM),
                    bordercolor=AppStyles.BORDER_COLOR,
                    lightcolor=AppStyles.CARD_BG_COLOR, # For border effect
                    darkcolor=AppStyles.CARD_BG_COLOR) # For border effect

        # Button style
        s.configure(AppStyles.TTK_BUTTON_STYLE,
                    font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_MEDIUM, "bold"),
                    background=AppStyles.PRIMARY_COLOR,
                    foreground="white",
                    relief="flat",
                    padding=(AppStyles.BUTTON_PAD_X, AppStyles.BUTTON_PAD_Y))
        s.map(AppStyles.TTK_BUTTON_STYLE,
              background=[('active', AppStyles.PRIMARY_COLOR)], # Keep consistent on click
              foreground=[('active', 'white')])

        # Special button styles
        s.configure('Add.TButton', background=AppStyles.PRIMARY_COLOR, foreground='white')
        s.map('Add.TButton', background=[('active', AppStyles.PRIMARY_COLOR)])

        s.configure('Delete.TButton', background=AppStyles.DELETE_COLOR, foreground='white')
        s.map('Delete.TButton', background=[('active', AppStyles.DELETE_COLOR)])

        s.configure('Toggle.TButton', background=AppStyles.ACCENT_COLOR, foreground='white')
        s.map('Toggle.TButton', background=[('active', AppStyles.ACCENT_COLOR)])

        # Label style
        s.configure(AppStyles.TTK_LABEL_STYLE,
                    background=AppStyles.BG_COLOR,
                    foreground=AppStyles.TEXT_COLOR,
                    font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_MEDIUM))

        # Combobox (Dropdown) style
        s.configure(AppStyles.TTK_COMBOBOX_STYLE,
                    fieldbackground=AppStyles.CARD_BG_COLOR,
                    background=AppStyles.CARD_BG_COLOR,
                    foreground=AppStyles.TEXT_COLOR,
                    font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_MEDIUM),
                    selectbackground=AppStyles.PRIMARY_COLOR,
                    selectforeground='white',
                    bordercolor=AppStyles.BORDER_COLOR)
        s.map(AppStyles.TTK_COMBOBOX_STYLE,
              background=[('readonly', AppStyles.CARD_BG_COLOR)]) # Ensure it's white when not active

        # Checkbutton style
        s.configure(AppStyles.TTK_CHECKBUTTON_STYLE,
                    background=AppStyles.BG_COLOR,
                    foreground=AppStyles.TEXT_COLOR,
                    font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_MEDIUM),
                    indicatorcolor=AppStyles.PRIMARY_COLOR, # Color of the square
                    indicatordiameter=15) # Size of the square
        s.map(AppStyles.TTK_CHECKBUTTON_STYLE,
              background=[('active', AppStyles.BG_COLOR)], # No change on active
              foreground=[('active', AppStyles.TEXT_COLOR)])

        # Listbox style (Tkinter Listbox is hard to style with ttk)
        # We will manually configure the tk.Listbox in _create_widgets
        # or consider using a ttk.Treeview for more control, but it's complex for simple list.

    def _create_widgets(self):
        # --- Input Frame ---
        self.input_frame = ttk.Frame(self.master, padding=AppStyles.PADDING, style=AppStyles.TTK_FRAME_STYLE)

        tk.Label(self.input_frame, text="Description:", font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_SMALL), bg=AppStyles.BG_COLOR).grid(row=0, column=0, sticky="w", pady=(0,2))
        self.task_description_entry = ttk.Entry(self.input_frame, width=40, style=AppStyles.TTK_ENTRY_STYLE)
        self.task_description_entry.grid(row=1, column=0, columnspan=2, padx=(0,5), pady=(0,10), sticky="ew")
        self.task_description_entry.bind("<Return>", lambda event: self.add_task())

        tk.Label(self.input_frame, text="Category:", font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_SMALL), bg=AppStyles.BG_COLOR).grid(row=2, column=0, sticky="w", pady=(0,2))
        self.task_category_entry = ttk.Entry(self.input_frame, width=20, style=AppStyles.TTK_ENTRY_STYLE)
        self.task_category_entry.grid(row=3, column=0, padx=(0,5), pady=(0,10), sticky="ew")

        tk.Label(self.input_frame, text="Due Date (YYYY-MM-DD):", font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_SMALL), bg=AppStyles.BG_COLOR).grid(row=2, column=1, sticky="w", pady=(0,2))
        self.task_due_date_entry = ttk.Entry(self.input_frame, width=20, style=AppStyles.TTK_ENTRY_STYLE)
        self.task_due_date_entry.grid(row=3, column=1, padx=(0,5), pady=(0,10), sticky="ew")

        self.add_button = ttk.Button(self.input_frame, text="Add Task", command=self.add_task, style='Add.TButton')
        self.add_button.grid(row=4, column=0, columnspan=2, pady=(5,0), sticky="ew")

        # --- Controls Frame (Filter/Sort) ---
        self.controls_frame = ttk.Frame(self.master, padding=(AppStyles.PADDING, AppStyles.PADDING, AppStyles.PADDING, 0), style=AppStyles.TTK_FRAME_STYLE)

        tk.Label(self.controls_frame, text="Filter Category:", font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_SMALL), bg=AppStyles.BG_COLOR).grid(row=0, column=0, sticky="w", padx=(0,5))
        self.category_filter_combobox = ttk.Combobox(self.controls_frame, state="readonly", width=15, style=AppStyles.TTK_COMBOBOX_STYLE)
        self.category_filter_combobox.grid(row=1, column=0, sticky="ew", padx=(0,10))
        self.category_filter_combobox.bind("<<ComboboxSelected>>", self._load_tasks_to_listbox) # Reload on selection

        tk.Label(self.controls_frame, text="Sort By:", font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_SMALL), bg=AppStyles.BG_COLOR).grid(row=0, column=1, sticky="w", padx=(0,5))
        self.sort_by_combobox = ttk.Combobox(self.controls_frame, state="readonly", width=15, style=AppStyles.TTK_COMBOBOX_STYLE,
                                             values=["Creation Date", "Due Date", "Description", "Status"])
        self.sort_by_combobox.set("Creation Date") # Default value
        self.sort_by_combobox.grid(row=1, column=1, sticky="ew", padx=(0,10))
        self.sort_by_combobox.bind("<<ComboboxSelected>>", self._load_tasks_to_listbox)

        self.include_completed_var = tk.BooleanVar(value=True)
        self.include_completed_checkbutton = ttk.Checkbutton(
            self.controls_frame,
            text="Show Completed",
            variable=self.include_completed_var,
            command=self._load_tasks_to_listbox,
            style=AppStyles.TTK_CHECKBUTTON_STYLE
        )
        self.include_completed_checkbutton.grid(row=1, column=2, sticky="e", padx=(0,5))
        self.controls_frame.grid_columnconfigure(0, weight=1)
        self.controls_frame.grid_columnconfigure(1, weight=1)
        self.controls_frame.grid_columnconfigure(2, weight=1)

        # --- Task List Frame ---
        self.list_frame = ttk.Frame(self.master, padding=AppStyles.PADDING, style=AppStyles.TTK_FRAME_STYLE)
        self.task_listbox = tk.Listbox(
            self.list_frame,
            width=50,
            height=15,
            font=(AppStyles.FONT_FAMILY, AppStyles.FONT_SIZE_MEDIUM),
            bg=AppStyles.CARD_BG_COLOR,
            fg=AppStyles.TEXT_COLOR,
            selectbackground=AppStyles.PRIMARY_COLOR,
            selectforeground="#FFFFFF",
            bd=0, # No border
            highlightthickness=0, # No highlight border on focus
            relief="flat",
            activestyle='none' # No special style on active item
        )
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Map internal task IDs to listbox indices
        self.task_id_map = {} # {listbox_index: task_id}

        # --- Action Buttons Frame ---
        self.action_button_frame = ttk.Frame(self.master, padding=AppStyles.PADDING, style=AppStyles.TTK_FRAME_STYLE)

        self.delete_button = ttk.Button(self.action_button_frame, text="Delete Selected", command=self.delete_selected_task, style='Delete.TButton')
        self.delete_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, AppStyles.PADDING))

        self.toggle_button = ttk.Button(self.action_button_frame, text="Toggle Status", command=self.toggle_selected_task_status, style='Toggle.TButton')
        self.toggle_button.pack(side=tk.LEFT, expand=True, fill=tk.X)

    def _layout_widgets(self):
        self.input_frame.pack(pady=AppStyles.PADDING, fill=tk.X)
        self.controls_frame.pack(pady=(0, AppStyles.PADDING), fill=tk.X)
        self.list_frame.pack(pady=(0, AppStyles.PADDING), fill=tk.BOTH, expand=True)
        self.action_button_frame.pack(pady=(0, AppStyles.PADDING), fill=tk.X)

    def _load_tasks_to_listbox(self, event=None): # event parameter for combobox binding
        self.task_listbox.delete(0, tk.END)
        self.task_id_map = {} # Reset map

        # Get filter/sort criteria
        selected_category = self.category_filter_combobox.get()
        if selected_category == "All" or not selected_category:
            selected_category = None # Pass None to get_tasks to signify no category filter

        sort_by_mapping = {
            "Creation Date": "created_at",
            "Due Date": "due_date",
            "Description": "description",
            "Status": "completed"
        }
        current_sort_by = sort_by_mapping.get(self.sort_by_combobox.get(), 'created_at')
        include_completed = self.include_completed_var.get()

        tasks = self.task_manager.get_tasks(
            category=selected_category,
            include_completed=include_completed,
            sort_by=current_sort_by
        )

        today = datetime.date.today()

        for i, task in enumerate(tasks):
            self.task_id_map[i] = task['id'] # Map listbox index to task ID

            display_text = f"{task['description']}"
            meta_info = []

            # Add category if available
            if task.get('category') and task['category'] != 'Uncategorized':
                meta_info.append(f"Cat: {task['category']}")

            # Add due date if available and check overdue status
            if task.get('due_date'):
                try:
                    due_date_dt = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                    if not task['completed'] and due_date_dt < today:
                        meta_info.append(f"DUE: {task['due_date']} (OVERDUE!)")
                    else:
                        meta_info.append(f"Due: {task['due_date']}")
                except ValueError:
                    meta_info.append(f"Due: Invalid Date")

            # Add creation date
            if task.get('created_at'):
                try:
                    created_date_dt = datetime.datetime.fromisoformat(task['created_at']).date()
                    meta_info.append(f"Created: {created_date_dt.strftime('%Y-%m-%d')}")
                except ValueError:
                    meta_info.append(f"Created: Invalid Date")

            full_display_text = display_text
            if meta_info:
                full_display_text += f" ({', '.join(meta_info)})"

            self.task_listbox.insert(tk.END, full_display_text)

            # Apply styling based on task status and overdue
            if task['completed']:
                self.task_listbox.itemconfig(i, {'fg': AppStyles.COMPLETED_TEXT_COLOR})
                self.task_listbox.itemconfigure(i, bg=AppStyles.BG_COLOR) # Light grey for completed background
            elif task.get('due_date'):
                 try:
                    due_date_dt = datetime.datetime.strptime(task['due_date'], '%Y-%m-%d').date()
                    if due_date_dt < today:
                         self.task_listbox.itemconfig(i, {'fg': AppStyles.OVERDUE_COLOR})
                         self.task_listbox.itemconfigure(i, bg="#FFEBEB") # Light red for overdue background
                    else:
                        self.task_listbox.itemconfig(i, {'fg': AppStyles.TEXT_COLOR})
                        self.task_listbox.itemconfigure(i, bg=AppStyles.CARD_BG_COLOR) # Default white
                 except ValueError:
                    self.task_listbox.itemconfig(i, {'fg': AppStyles.TEXT_COLOR})
                    self.task_listbox.itemconfigure(i, bg=AppStyles.CARD_BG_COLOR) # Default white
            else:
                self.task_listbox.itemconfig(i, {'fg': AppStyles.TEXT_COLOR})
                self.task_listbox.itemconfigure(i, bg=AppStyles.CARD_BG_COLOR) # Default white


        # Update category filter dropdown values
        all_categories = self.task_manager.get_categories()
        self.category_filter_combobox['values'] = ['All'] + all_categories
        if selected_category is None: # If 'All' was selected or no filter previously
            self.category_filter_combobox.set('All')
        elif selected_category not in all_categories and selected_category is not None:
             # If previously selected category no longer exists, reset to 'All'
            self.category_filter_combobox.set('All')
            self._load_tasks_to_listbox() # Recurse to reload with 'All' filter

    def add_task(self):
        description = self.task_description_entry.get()
        category = self.task_category_entry.get()
        due_date = self.task_due_date_entry.get()

        if self.task_manager.add_task(description, category, due_date):
            self.task_description_entry.delete(0, tk.END)
            self.task_category_entry.delete(0, tk.END)
            self.task_due_date_entry.delete(0, tk.END)
            self._load_tasks_to_listbox()
        else:
            messagebox.showwarning("Input Error", "Task description cannot be empty!")

    def delete_selected_task(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_id_to_delete = self.task_id_map.get(selected_index)

            if task_id_to_delete:
                if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete the selected task?"):
                    if self.task_manager.delete_task(task_id_to_delete):
                        self._load_tasks_to_listbox()
                    else:
                        messagebox.showerror("Error", "Failed to delete task.")
            else:
                messagebox.showwarning("Selection Error", "Please select a task to delete.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def toggle_selected_task_status(self):
        try:
            selected_index = self.task_listbox.curselection()[0]
            task_id_to_toggle = self.task_id_map.get(selected_index)

            if task_id_to_toggle:
                if self.task_manager.toggle_task_status(task_id_to_toggle):
                    self._load_tasks_to_listbox()
                else:
                    messagebox.showerror("Error", "Failed to toggle task status.")
            else:
                messagebox.showwarning("Selection Error", "Please select a task to toggle its status.")
        except IndexError:
            messagebox.showwarning("Selection Error", "Please select a task to toggle its status.")