"""
User History Manager Module
Tracks user recommendations and analysis history
"""
import logging
import pymysql
import json
from dotenv import load_dotenv
import os

logger = logging.getLogger(__name__)
load_dotenv()


class HistoryManager:
    """
    Manages user history and recommendation tracking
    """
    
    def __init__(self):
        """Initialize history manager with MySQL connection"""
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
    
    def save_recommendation(self, user_id, input_params, recommendation):
        """
        Save user's recommendation to history
        
        Args:
            user_id: ID of the user
            input_params: Dictionary of input parameters
            recommendation: Dictionary with recommendation results
        
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            query = """
            INSERT INTO user_history 
            (user_id, nitrogen, phosphorus, potassium, temperature, temperature_unit, 
             humidity, rainfall, ph, season, location, recommended_crop, confidence, 
             alternatives, reasoning, seasonal_note)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            params = (
                user_id,
                input_params.get('nitrogen'),
                input_params.get('phosphorus'),
                input_params.get('potassium'),
                input_params.get('temperature'),
                input_params.get('temperature_unit', 'C'),
                input_params.get('humidity'),
                input_params.get('rainfall'),
                input_params.get('ph'),
                input_params.get('season'),
                input_params.get('location'),
                recommendation.get('primary_crop'),
                recommendation.get('confidence'),
                json.dumps(recommendation.get('alternatives', [])),
                recommendation.get('reasoning', ''),
                recommendation.get('seasonal_note', '')
            )
            
            cursor.execute(query, params)
            conn.commit()
            
            logger.info(f"Recommendation saved to history for user: {user_id}")
            return True, "Recommendation saved"
        
        except Exception as e:
            logger.error(f"Error saving recommendation: {e}")
            return False, f"Error: {str(e)}"
        finally:
            cursor.close()
            conn.close()
    
    def get_user_history(self, user_id, limit=50):
        """
        Get recommendation history for a user
        
        Args:
            user_id: ID of the user
            limit: Number of records to retrieve
        
        Returns:
            list: List of recommendation records
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            query = """
            SELECT * FROM user_history 
            WHERE user_id = %s 
            ORDER BY created_at DESC 
            LIMIT %s
            """
            
            cursor.execute(query, (user_id, limit))
            history = cursor.fetchall()
            
            # Parse JSON fields
            for record in history:
                if record.get('alternatives'):
                    record['alternatives'] = json.loads(record['alternatives'])
            
            return history
        
        except Exception as e:
            logger.error(f"Error retrieving history: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def get_history_stats(self, user_id):
        """
        Get statistics about user's recommendation history
        
        Args:
            user_id: ID of the user
        
        Returns:
            dict: Statistics about recommendations
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Total recommendations
            cursor.execute("SELECT COUNT(*) as total FROM user_history WHERE user_id = %s", (user_id,))
            total = cursor.fetchone()[0]
            
            # Most recommended crops
            cursor.execute("""
                SELECT recommended_crop, COUNT(*) as count 
                FROM user_history 
                WHERE user_id = %s 
                GROUP BY recommended_crop 
                ORDER BY count DESC 
                LIMIT 5
            """, (user_id,))
            top_crops = cursor.fetchall()
            
            # Average confidence
            cursor.execute(
                "SELECT AVG(confidence) as avg_confidence FROM user_history WHERE user_id = %s",
                (user_id,)
            )
            avg_confidence = cursor.fetchone()[0]
            
            return {
                'total_recommendations': total,
                'top_crops': [{'crop': crop[0], 'count': crop[1]} for crop in top_crops],
                'average_confidence': round(avg_confidence, 2) if avg_confidence else 0
            }
        
        except Exception as e:
            logger.error(f"Error getting stats: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()
    
    def delete_history_record(self, user_id, record_id):
        """Delete a specific history record"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Verify ownership
            cursor.execute("SELECT user_id FROM user_history WHERE id = %s", (record_id,))
            result = cursor.fetchone()
            
            if not result or result[0] != user_id:
                return False, "Unauthorized"
            
            cursor.execute("DELETE FROM user_history WHERE id = %s", (record_id,))
            conn.commit()
            
            return True, "Record deleted"
        
        except Exception as e:
            logger.error(f"Error deleting record: {e}")
            return False, f"Error: {str(e)}"
        finally:
            cursor.close()
            conn.close()
