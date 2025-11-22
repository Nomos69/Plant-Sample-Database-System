"""
Delete operation module for Plant Sample CRUD Application.

Handles DELETE operations for removing plant samples from the database.
"""

from config import TABLE_PLANT_SAMPLE, COL_SAMPLE_ID


def delete_sample(cursor, conn, sample_id):
    """
    Delete a plant sample from the database by its ID.
    
    Args:
        cursor: Database cursor
        conn: Database connection
        sample_id (str): Unique identifier for the sample
        
    Returns:
        tuple: (success: bool, message: str)
        - (True, "Sample deleted successfully") on success
        - (False, "Sample ID not found") if sample doesn't exist
        - (False, error_message) on other database errors
    """
    try:
        cursor.execute(f'DELETE FROM "{TABLE_PLANT_SAMPLE}" WHERE "{COL_SAMPLE_ID}" = %s', (sample_id,))
        conn.commit()
        
        if cursor.rowcount > 0:
            return True, "Sample deleted successfully"
        else:
            return False, "Sample ID not found"
    except Exception as e:
        conn.rollback()
        return False, str(e)
