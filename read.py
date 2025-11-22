"""
Read operation module for Plant Sample CRUD Application.

Handles SELECT operations for querying plant samples from the database.
"""

from config import TABLE_PLANT_SAMPLE, COL_SAMPLE_ID, COL_SAMPLE_ATTRIBUTES, COL_RESEARCHER_ID, COL_LOCATION_ID


def query_sample(cursor, conn, sample_id):
    """
    Query a specific plant sample by its ID.
    
    Args:
        cursor: Database cursor
        conn: Database connection
        sample_id (str): Unique identifier for the sample
        
    Returns:
        tuple: (sample_id, sample_attributes, researcher_id, location_id) or None
        
    Raises:
        Exception: If database query fails
    """
    try:
        cursor.execute(f'''
            SELECT "{COL_SAMPLE_ID}", "{COL_SAMPLE_ATTRIBUTES}", "{COL_RESEARCHER_ID}", "{COL_LOCATION_ID}"
            FROM "{TABLE_PLANT_SAMPLE}"
            WHERE "{COL_SAMPLE_ID}" = %s
        ''', (sample_id,))
        
        result = cursor.fetchone()
        return result
    except Exception as e:
        raise Exception(f"Query failed: {str(e)}")


def get_all_samples(cursor, conn):
    """
    Retrieve all plant samples from the database.
    
    Args:
        cursor: Database cursor
        conn: Database connection
        
    Returns:
        list: List of tuples containing (sample_id, researcher_id, location_id, sample_attributes)
        
    Raises:
        Exception: If database query fails
    """
    try:
        cursor.execute(f'SELECT "{COL_SAMPLE_ID}", "{COL_RESEARCHER_ID}", "{COL_LOCATION_ID}", "{COL_SAMPLE_ATTRIBUTES}" FROM "{TABLE_PLANT_SAMPLE}"')
        rows = cursor.fetchall()
        return rows
    except Exception as e:
        raise Exception(f"Failed to fetch samples:\n{str(e)}")
