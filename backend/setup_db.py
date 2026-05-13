"""
Database Setup Script
Creates the agri_expert_system database and required tables if they do not exist.
Run this script before starting the app when using MySQL.
"""
import os
import logging
import pymysql
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()


def get_db_config():
    return {
        'host': os.getenv('MYSQL_HOST', 'localhost'),
        'port': int(os.getenv('MYSQL_PORT', 3306)),
        'user': os.getenv('MYSQL_USER', 'root'),
        'password': os.getenv('MYSQL_PASSWORD', ''),
        'database': os.getenv('MYSQL_DB', 'agri_expert_system')
    }


def create_database(config):
    connection = None
    try:
        connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{config['database']}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
            logger.info(f"Database '{config['database']}' created or already exists.")
        connection.commit()
    finally:
        if connection:
            connection.close()


def create_tables(config):
    connection = None
    try:
        connection = pymysql.connect(
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            cursorclass=pymysql.cursors.DictCursor
        )
        with connection.cursor() as cursor:
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(128) NOT NULL UNIQUE,
                email VARCHAR(255) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                first_name VARCHAR(128),
                last_name VARCHAR(128),
                location VARCHAR(255),
                soil_type VARCHAR(128),
                farm_size VARCHAR(128),
                photo_url VARCHAR(500),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_history (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id INT NOT NULL,
                nitrogen FLOAT,
                phosphorus FLOAT,
                potassium FLOAT,
                temperature FLOAT,
                temperature_unit VARCHAR(8),
                humidity FLOAT,
                rainfall FLOAT,
                ph FLOAT,
                season VARCHAR(64),
                location VARCHAR(255),
                recommended_crop VARCHAR(128),
                confidence FLOAT,
                alternatives JSON,
                reasoning TEXT,
                seasonal_note TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                INDEX idx_user_id (user_id),
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            cursor.execute("""
            CREATE TABLE IF NOT EXISTS feedback (
                id INT AUTO_INCREMENT PRIMARY KEY,
                original_input JSON,
                recommendation JSON,
                accuracy VARCHAR(64),
                comment TEXT,
                actual_crop VARCHAR(128),
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """)

            logger.info("Required tables created or already exist.")
        connection.commit()
    finally:
        if connection:
            connection.close()


def main():
    config = get_db_config()
    create_database(config)
    create_tables(config)
    logger.info("Database setup completed successfully.")


if __name__ == '__main__':
    main()
