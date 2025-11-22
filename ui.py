"""
User interface module for Plant Sample CRUD Application.

Provides PlantSampleUI class that creates and manages the Tkinter GUI
for the plant sample database management system.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import json
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, FONT_TITLE, PADDING


class PlantSampleUI:
    """
    Manages the user interface for the Plant Sample CRUD application.
    
    Provides GUI components for:
    - Adding new plant samples
    - Querying existing samples by ID
    - Updating sample information
    - Deleting samples
    - Displaying all samples in a table
    """
    
    def __init__(self, root, db_manager):
        """
        Initialize the UI with main window and database manager.
        
        Args:
            root: Tkinter root window
            db_manager: DatabaseManager instance for database operations
        """
        self.root = root
        self.db_manager = db_manager
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")
        
        self.query_id = None
        self.sample_id = None
        self.researcher_id = None
        self.location_id = None
        self.sample_attr = None
        self.tree = None
        
        self.create_widgets()
        self.refresh_table()
    
    def create_widgets(self):
        """Initialize and layout all UI widgets."""
        main_frame = ttk.Frame(self.root, padding=PADDING)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        title = ttk.Label(main_frame, text=APP_TITLE, font=FONT_TITLE)
        title.grid(row=0, column=0, columnspan=4, pady=10)
        
        self._create_query_section(main_frame)
        self._create_form_section(main_frame)
        self._create_buttons(main_frame)
        self._create_table_section(main_frame)
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(4, weight=1)
    
    def _create_query_section(self, parent):
        """Create the query sample section."""
        query_frame = ttk.LabelFrame(parent, text="Query Sample", padding=PADDING)
        query_frame.grid(row=1, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(query_frame, text="Sample ID:").grid(row=0, column=0, padx=5)
        self.query_id = ttk.Entry(query_frame, width=20)
        self.query_id.grid(row=0, column=1, padx=5)
        ttk.Button(query_frame, text="Query", command=self.query_sample).grid(row=0, column=2, padx=5)
    
    def _create_form_section(self, parent):
        """Create the add/update form section."""
        form_frame = ttk.LabelFrame(parent, text="Add/Update Sample", padding=PADDING)
        form_frame.grid(row=2, column=0, columnspan=4, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(form_frame, text="Sample ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.sample_id = ttk.Entry(form_frame, width=30)
        self.sample_id.grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Researcher ID:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.researcher_id = ttk.Entry(form_frame, width=30)
        self.researcher_id.grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Location ID:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        self.location_id = ttk.Entry(form_frame, width=30)
        self.location_id.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(form_frame, text="Sample Attributes (JSON):").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        self.sample_attr = ttk.Entry(form_frame, width=30)
        self.sample_attr.grid(row=1, column=3, padx=5, pady=5)
    
    def _create_buttons(self, parent):
        """Create action buttons (Add, Update, Delete, Clear)."""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=3, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Add", command=self.add_sample).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Update", command=self.update_sample).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Delete", command=self.delete_sample).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_form).grid(row=0, column=3, padx=5)
    
    def _create_table_section(self, parent):
        """Create the table display section for all samples."""
        table_frame = ttk.Frame(parent)
        table_frame.grid(row=4, column=0, columnspan=4, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        scrollbar = ttk.Scrollbar(table_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(table_frame, 
                                 columns=('Sample ID', 'Researcher ID', 'Location ID', 'Sample Attributes'),
                                 show='headings', yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading('Sample ID', text='Sample ID')
        self.tree.heading('Researcher ID', text='Researcher ID')
        self.tree.heading('Location ID', text='Location ID')
        self.tree.heading('Sample Attributes', text='Sample Attributes')
        
        self.tree.column('Sample ID', width=100)
        self.tree.column('Researcher ID', width=120)
        self.tree.column('Location ID', width=100)
        self.tree.column('Sample Attributes', width=300)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind('<ButtonRelease-1>', self.on_select)
    
    def add_sample(self):
        """Handle add sample button click - insert new sample into database."""
        sample_id = self.sample_id.get()
        researcher_id = self.researcher_id.get() or None
        location_id = self.location_id.get() or None
        sample_attr = self.sample_attr.get() or "{}"
        
        if not sample_id:
            messagebox.showerror("Error", "Sample ID is required")
            return
        
        if not self._validate_json(sample_attr):
            return
        
        success, message = self.db_manager.add_sample(sample_id, researcher_id, location_id, sample_attr)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_table()
        else:
            messagebox.showerror("Error", message)
    
    def update_sample(self):
        """Handle update sample button click - modify existing sample."""
        sample_id = self.sample_id.get()
        researcher_id = self.researcher_id.get() or None
        location_id = self.location_id.get() or None
        sample_attr = self.sample_attr.get() or "{}"
        
        if not sample_id:
            messagebox.showerror("Error", "Sample ID is required")
            return
        
        if not self._validate_json(sample_attr):
            return
        
        success, message = self.db_manager.update_sample(sample_id, researcher_id, location_id, sample_attr)
        
        if success:
            messagebox.showinfo("Success", message)
            self.clear_form()
            self.refresh_table()
        else:
            messagebox.showerror("Error", message)
    
    def delete_sample(self):
        """Handle delete sample button click - remove sample from database."""
        sample_id = self.sample_id.get()
        
        if not sample_id:
            messagebox.showerror("Error", "Sample ID is required")
            return
        
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this sample?"):
            success, message = self.db_manager.delete_sample(sample_id)
            
            if success:
                messagebox.showinfo("Success", message)
                self.clear_form()
                self.refresh_table()
            else:
                messagebox.showerror("Error", message)
    
    def query_sample(self):
        """Query a specific sample and display results in JSON format."""
        sample_id = self.query_id.get()
        
        if not sample_id:
            messagebox.showerror("Error", "Sample ID is required")
            return
        
        try:
            result = self.db_manager.query_sample(sample_id)
            
            if result:
                result_dict = {
                    "Sample ID": result[0],
                    "Sample Attributes": result[1] if result[1] else {},
                    "Researcher ID": result[2],
                    "Location ID": result[3]
                }
                json_result = json.dumps(result_dict, indent=2)
                messagebox.showinfo("Query Result", json_result)
            else:
                messagebox.showinfo("Query Result", "Sample not found")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def refresh_table(self):
        """Refresh the table display with all samples from the database."""
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        try:
            rows = self.db_manager.get_all_samples()
            
            for row in rows:
                display_row = list(row)
                if display_row[3]:
                    display_row[3] = json.dumps(display_row[3])
                self.tree.insert('', tk.END, values=display_row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def on_select(self, event):
        """Handle table row selection - populate form fields with selected row data."""
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected[0])['values']
            self.sample_id.delete(0, tk.END)
            self.sample_id.insert(0, values[0])
            
            self.researcher_id.delete(0, tk.END)
            if values[1]:
                self.researcher_id.insert(0, values[1])
            
            self.location_id.delete(0, tk.END)
            if values[2]:
                self.location_id.insert(0, values[2])
            
            self.sample_attr.delete(0, tk.END)
            if values[3]:
                self.sample_attr.insert(0, values[3])
    
    def clear_form(self):
        """Clear all form input fields."""
        self.sample_id.delete(0, tk.END)
        self.researcher_id.delete(0, tk.END)
        self.location_id.delete(0, tk.END)
        self.sample_attr.delete(0, tk.END)
        self.query_id.delete(0, tk.END)
    
    @staticmethod
    def _validate_json(json_string):
        """
        Validate if a string is valid JSON format.
        
        Args:
            json_string (str): String to validate
            
        Returns:
            bool: True if valid JSON, False otherwise. Shows error message on invalid JSON.
        """
        try:
            json.loads(json_string)
            return True
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON format for Sample Attributes")
            return False
