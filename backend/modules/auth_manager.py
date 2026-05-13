"""
Authentication Manager Module
Handles user registration, login, and session management
"""
import logging
import pymysql
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
load_dotenv()


class AuthManager:
    """
    Manages user authentication and account management
    """
    
    def __init__(self):
        """Initialize auth manager with MySQL connection"""
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.port = int(os.getenv('MYSQL_PORT', 3306))
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', '')
        self.db = os.getenv('MYSQL_DB', 'agri_expert_system')
    
    def _get_connection(self):
        """Get MySQL connection"""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db
        )
    
    def register_user(self, username, email, password, first_name='', last_name=''):
        """
        Register a new user
        
        Args:
            username: Username for the account
            email: User email address
            password: Plain text password (will be hashed)
            first_name: User's first name
            last_name: User's last name
        
        Returns:
            tuple: (success: bool, message: str, user_id: int or None)
        """
        try:
            # Validate inputs
            if not username or not email or not password:
                return False, "All fields are required", None
            
            if len(password) < 6:
                return False, "Password must be at least 6 characters", None
            
            # Hash password
            hashed_password = generate_password_hash(password)
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT id FROM users WHERE username = %s OR email = %s", (username, email))
            if cursor.fetchone():
                return False, "Username or email already exists", None
            
            # Insert new user
            query = """
            INSERT INTO users (username, email, password, first_name, last_name)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (username, email, hashed_password, first_name, last_name))
            conn.commit()
            
            user_id = cursor.lastrowid
            logger.info(f"User registered: {username} (ID: {user_id})")
            
            return True, "Registration successful", user_id
        
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, f"Registration failed: {str(e)}", None
        finally:
            cursor.close()
            conn.close()
    
    def login_user(self, username, password):
        """
        Authenticate user with username and password
        
        Args:
            username: Username
            password: Plain text password
        
        Returns:
            tuple: (success: bool, message: str, user_data: dict or None)
        """
        try:
            if not username or not password:
                return False, "Username and password are required", None
            
            conn = self._get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            # Get user from database
            cursor.execute(
                "SELECT id, username, email, password, first_name, last_name, location, farm_size, soil_type, photo_url FROM users WHERE username = %s OR email = %s",
                (username, username)
            )
            user = cursor.fetchone()
            
            if not user:
                return False, "Invalid username or password", None
            
            # Check password
            if not check_password_hash(user['password'], password):
                return False, "Invalid username or password", None
            
            # Remove password from response
            user_data = {k: v for k, v in user.items() if k != 'password'}
            
            logger.info(f"User logged in: {username}")
            return True, "Login successful", user_data
        
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False, f"Login failed: {str(e)}", None
        finally:
            cursor.close()
            conn.close()
    
    def get_user_by_id(self, user_id):
        """Get user data by ID"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            cursor.execute(
                "SELECT id, username, email, first_name, last_name, location, farm_size, soil_type, photo_url, created_at FROM users WHERE id = %s",
                (user_id,)
            )
            user = cursor.fetchone()
            
            return user
        
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            return None
        finally:
            cursor.close()
            conn.close()
    
    def update_user_profile(self, user_id, first_name=None, last_name=None, location=None, farm_size=None, soil_type=None, photo_url=None):
        """Update user profile information"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            updates = []
            params = []
            
            if first_name is not None:
                updates.append("first_name = %s")
                params.append(first_name)
            
            if last_name is not None:
                updates.append("last_name = %s")
                params.append(last_name)
            
            if location is not None:
                updates.append("location = %s")
                params.append(location)
            
            if farm_size is not None:
                updates.append("farm_size = %s")
                params.append(farm_size)
            
            if soil_type is not None:
                updates.append("soil_type = %s")
                params.append(soil_type)
            
            if photo_url:
                updates.append("photo_url = %s")
                params.append(photo_url)
            
            if not updates:
                return True, "No updates provided"
            
            params.append(user_id)
            query = f"UPDATE users SET {', '.join(updates)} WHERE id = %s"
            
            cursor.execute(query, params)
            conn.commit()
            
            logger.info(f"User profile updated: {user_id}")
            return True, "Profile updated successfully"
        
        except Exception as e:
            logger.error(f"Error updating profile: {e}")
            return False, f"Update failed: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    def change_password(self, user_id, old_password, new_password):
        """Change user password"""
        try:
            if not new_password or len(new_password) < 6:
                return False, "New password must be at least 6 characters"
            
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get current password hash
            cursor.execute("SELECT password FROM users WHERE id = %s", (user_id,))
            result = cursor.fetchone()
            
            if not result:
                return False, "User not found"
            
            # Verify old password
            if not check_password_hash(result[0], old_password):
                return False, "Current password is incorrect"
            
            # Hash and update new password
            new_hash = generate_password_hash(new_password)
            cursor.execute("UPDATE users SET password = %s WHERE id = %s", (new_hash, user_id))
            conn.commit()
            
            logger.info(f"Password changed for user: {user_id}")
            return True, "Password changed successfully"
        
        except Exception as e:
            logger.error(f"Error changing password: {e}")
            return False, f"Password change failed: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    def delete_user_account(self, user_id):
        """Delete user account and related data"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Delete user history first (foreign key constraint)
            cursor.execute("DELETE FROM user_history WHERE user_id = %s", (user_id,))
            
            # Delete user account
            cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
            conn.commit()
            
            logger.info(f"User account deleted: {user_id}")
            return True, "Account deleted successfully"
        
        except Exception as e:
            logger.error(f"Error deleting account: {e}")
            return False, f"Account deletion failed: {str(e)}"
        finally:
            cursor.close()
            conn.close()
