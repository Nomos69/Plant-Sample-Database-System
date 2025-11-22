"""
Create operation module for Plant Sample CRUD Application.

Handles INSERT operations for adding new plant samples to the database.
"""

import psycopg2
from config import TABLE_PLANT_SAMPLE, COL_SAMPLE_ID, COL_SAMPLE_ATTRIBUTES, COL_RESEARCHER_ID, COL_LOCATION_ID


def add_sample(cursor, conn, sample_id, researcher_id, location_id, sample_attr):
    """
    Insert a new plant sample into the database.
    
    Args:
        cursor: Database cursor
        conn: Database connection
        sample_id (str): Unique identifier for the sample
        researcher_id (str): ID of the researcher
        location_id (str): ID of the sampling location
        sample_attr (str): JSON string containing sample attributes
        
    Returns:
        tuple: (success: bool, message: str)
        - (True, "Sample added successfully") on success
        - (False, "Sample ID already exists") on duplicate ID
        - (False, error_message) on other database errors
    """
    try:
        cursor.execute(f'''
            INSERT INTO "{TABLE_PLANT_SAMPLE}" ("{COL_SAMPLE_ID}", "{COL_SAMPLE_ATTRIBUTES}", "{COL_RESEARCHER_ID}", "{COL_LOCATION_ID}")
            VALUES (%s, %s::json, %s, %s)
        ''', (sample_id, sample_attr, researcher_id, location_id))
        conn.commit()
        return True, "Sample added successfully"
    except psycopg2.IntegrityError:
        conn.rollback()
        return False, "Sample ID already exists"
    except Exception as e:
        conn.rollback()
        return False, str(e)
