"""
Update operation module for Plant Sample CRUD Application.

Handles UPDATE operations for modifying existing plant samples in the database.
"""

from config import TABLE_PLANT_SAMPLE, COL_SAMPLE_ID, COL_SAMPLE_ATTRIBUTES, COL_RESEARCHER_ID, COL_LOCATION_ID


def update_sample(cursor, conn, sample_id, researcher_id, location_id, sample_attr):
    """
    Update an existing plant sample in the database.
    
    Args:
        cursor: Database cursor
        conn: Database connection
        sample_id (str): Unique identifier for the sample
        researcher_id (str): ID of the researcher
        location_id (str): ID of the sampling location
        sample_attr (str): JSON string containing sample attributes
        
    Returns:
        tuple: (success: bool, message: str)
        - (True, "Sample updated successfully") on success
        - (False, "Sample ID not found") if sample doesn't exist
        - (False, error_message) on other database errors
    """
    try:
        cursor.execute(f'''
            UPDATE "{TABLE_PLANT_SAMPLE}" 
            SET "{COL_SAMPLE_ATTRIBUTES}" = %s::json, "{COL_RESEARCHER_ID}" = %s, "{COL_LOCATION_ID}" = %s
            WHERE "{COL_SAMPLE_ID}" = %s
        ''', (sample_attr, researcher_id, location_id, sample_id))
        conn.commit()
        
        if cursor.rowcount > 0:
            return True, "Sample updated successfully"
        else:
            return False, "Sample ID not found"
    except Exception as e:
        conn.rollback()
        return False, str(e)
