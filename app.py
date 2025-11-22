"""
Main entry point for Plant Sample CRUD Application.

Run this file to start the application.
"""

import tkinter as tk
from tkinter import messagebox
from database import DatabaseManager
from ui import PlantSampleUI


def main():
    """
    Initialize and run the application.
    
    Creates the main Tkinter window, initializes the database manager,
    and starts the UI.
    """
    root = tk.Tk()
    
    try:
        db_manager = DatabaseManager()
        app = PlantSampleUI(root, db_manager)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Database Error", f"Failed to start application:\n{str(e)}")
        root.destroy()


if __name__ == "__main__":
    main()
