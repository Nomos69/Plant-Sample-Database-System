"""
Database module for Plant Sample CRUD Application.

Provides DatabaseManager class that manages database connections and delegates
CRUD operations to specialized operation modules (create, read, update, delete).
"""

import psycopg2
from config import DB_CONFIG
from create import add_sample
from read import query_sample, get_all_samples
from update import update_sample
from delete import delete_sample


class DatabaseManager:
    """
    Manages database connection and orchestrates CRUD operations.
    
    Acts as a facade to coordinate between the UI layer and individual
    operation modules. Maintains the database connection and provides
    methods for add, read, update, and delete operations.
    """
    
    def __init__(self):
        """Initialize database connection and cursor."""
        self.conn = None
        self.cursor = None
        self.connect()
    
    def connect(self):
        """
        Establish connection to PostgreSQL database.
        
        Raises:
            Exception: If database connection fails.
        """
        try:
            self.conn = psycopg2.connect(**DB_CONFIG)
            self.cursor = self.conn.cursor()
        except Exception as e:
            raise Exception(f"Failed to connect to database:\n{str(e)}")
    
    def add_sample(self, sample_id, researcher_id, location_id, sample_attr):
        """
        Add a new plant sample to the database.
        
        Args:
            sample_id (str): Unique identifier for the sample
            researcher_id (str): ID of the researcher
            location_id (str): ID of the sampling location
            sample_attr (str): JSON string containing sample attributes
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return add_sample(self.cursor, self.conn, sample_id, researcher_id, location_id, sample_attr)
    
    def update_sample(self, sample_id, researcher_id, location_id, sample_attr):
        """
        Update an existing plant sample.
        
        Args:
            sample_id (str): Unique identifier for the sample
            researcher_id (str): ID of the researcher
            location_id (str): ID of the sampling location
            sample_attr (str): JSON string containing sample attributes
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return update_sample(self.cursor, self.conn, sample_id, researcher_id, location_id, sample_attr)
    
    def delete_sample(self, sample_id):
        """
        Delete a plant sample by its ID.
        
        Args:
            sample_id (str): Unique identifier for the sample
            
        Returns:
            tuple: (success: bool, message: str)
        """
        return delete_sample(self.cursor, self.conn, sample_id)
    
    def query_sample(self, sample_id):
        """
        Query a specific plant sample by ID.
        
        Args:
            sample_id (str): Unique identifier for the sample
            
        Returns:
            tuple: (sample_id, sample_attributes, researcher_id, location_id) or None
        """
        return query_sample(self.cursor, self.conn, sample_id)
    
    def get_all_samples(self):
        """
        Retrieve all plant samples from the database.
        
        Returns:
            list: List of tuples containing (sample_id, researcher_id, location_id, sample_attributes)
        """
        return get_all_samples(self.cursor, self.conn)
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        self.close()
