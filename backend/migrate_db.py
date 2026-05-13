"""
Database Migration Script
Adds photo_url column to users table if it doesn't exist
Run this script once to update the database schema
"""
import pymysql
from dotenv import load_dotenv
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def migrate_database():
    """Add photo_url column to users table"""
    try:
        host = os.getenv('MYSQL_HOST', 'localhost')
        port = int(os.getenv('MYSQL_PORT', 3306))
        user = os.getenv('MYSQL_USER', 'root')
        password = os.getenv('MYSQL_PASSWORD', '')
        db = os.getenv('MYSQL_DB', 'agri_expert_system')
        
        conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=db
        )
        cursor = conn.cursor()
        
        # Check if photo_url column exists
        cursor.execute("""
            SELECT COLUMN_NAME 
            FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME='users' AND TABLE_SCHEMA=%s AND COLUMN_NAME='photo_url'
        """, (db,))
        
        if cursor.fetchone():
            logger.info("photo_url column already exists")
        else:
            # Add photo_url column if it doesn't exist
            cursor.execute("""
                ALTER TABLE users 
                ADD COLUMN photo_url VARCHAR(500) NULL
            """)
            conn.commit()
            logger.info("Successfully added photo_url column to users table")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Migration error: {str(e)}")
        raise

if __name__ == '__main__':
    migrate_database()
