"""
Configuration module for Plant Sample CRUD Application.

Contains all configuration constants including database connection parameters,
UI settings, and database table/column names.
"""

DB_CONFIG = {
    'dbname': 'plant_database',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '5432'
}

APP_TITLE = "Plant Sample Database System"
APP_WIDTH = 900
APP_HEIGHT = 600
FONT_TITLE = ('Arial', 16, 'bold')
PADDING = "10"

TABLE_PLANT_SAMPLE = "Plant Sample"
COL_SAMPLE_ID = "Sample ID"
COL_RESEARCHER_ID = "Researcher ID"
COL_LOCATION_ID = "Location ID"
COL_SAMPLE_ATTRIBUTES = "Sample Attributes"
