"""
Feedback Manager Module
Manages user feedback collection and storage for system improvement
"""
import json
import logging
from datetime import datetime
import os
import pymysql
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
load_dotenv()


class FeedbackManager:
    """
    Manages feedback from users about crop recommendations
    Stores feedback in MySQL database for future model improvement
    """
    
    def __init__(self):
        """Initialize feedback manager with MySQL connection"""
        self.host = os.getenv('MYSQL_HOST', 'localhost')
        self.port = int(os.getenv('MYSQL_PORT', 3306))
        self.user = os.getenv('MYSQL_USER', 'root')
        self.password = os.getenv('MYSQL_PASSWORD', '')
        self.db = os.getenv('MYSQL_DB', 'agri_expert_system')
        self._test_connection()
    
    def _test_connection(self):
        """Test MySQL connection"""
        try:
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.db
            )
            conn.close()
            logger.info("MySQL connection successful")
        except Exception as e:
            logger.error(f"MySQL connection failed: {e}")
            raise
    
    def _get_connection(self):
        """Get MySQL connection"""
        return pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.db
        )
    
    def save_feedback(self, feedback_data):
        """
        Save feedback from user to MySQL database
        
        Expected feedback_data format:
        {
            'original_input': {...},
            'recommendation': {
                'crop': 'Rice',
                'confidence': 85.5
            },
            'accuracy': 'accurate|somewhat_accurate|inaccurate',
            'comment': 'Optional comment from user',
            'actual_crop': 'Optional: what user actually planted'
        }
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            original_input = json.dumps(feedback_data.get('original_input', {}))
            recommendation = json.dumps(feedback_data.get('recommendation', {}))
            accuracy = feedback_data.get('accuracy', '')
            comment = feedback_data.get('comment', '')
            actual_crop = feedback_data.get('actual_crop', '')
            
            query = """
            INSERT INTO feedback 
            (original_input, recommendation, accuracy, comment, actual_crop) 
            VALUES (%s, %s, %s, %s, %s)
            """
            
            cursor.execute(query, (original_input, recommendation, accuracy, comment, actual_crop))
            conn.commit()
            
            logger.info(f"Feedback saved to MySQL database")
            return True
        
        except Exception as e:
            logger.error(f"Error saving feedback to MySQL: {e}")
            return False
        finally:
            cursor.close()
            conn.close()
    
    def get_all_feedback(self):
        """Retrieve all feedback from MySQL"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            query = "SELECT * FROM feedback ORDER BY timestamp DESC"
            cursor.execute(query)
            feedbacks = cursor.fetchall()
            
            # Parse JSON fields
            for f in feedbacks:
                if f.get('original_input'):
                    f['original_input'] = json.loads(f['original_input'])
                if f.get('recommendation'):
                    f['recommendation'] = json.loads(f['recommendation'])
            
            return feedbacks
        
        except Exception as e:
            logger.error(f"Error reading feedback from MySQL: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def get_feedback_stats(self):
        """Get statistics about feedback from MySQL"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get total count
            cursor.execute("SELECT COUNT(*) as total FROM feedback")
            total = cursor.fetchone()[0]
            
            if total == 0:
                return {
                    'total_feedbacks': 0,
                    'accurate': 0,
                    'somewhat_accurate': 0,
                    'inaccurate': 0,
                    'accuracy_rate': 0
                }
            
            # Get accuracy counts
            cursor.execute("SELECT COUNT(*) as count FROM feedback WHERE accuracy = 'accurate'")
            accurate = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as count FROM feedback WHERE accuracy = 'somewhat_accurate'")
            somewhat_accurate = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) as count FROM feedback WHERE accuracy = 'inaccurate'")
            inaccurate = cursor.fetchone()[0]
            
            accuracy_rate = (accurate / total) * 100
            
            return {
                'total_feedbacks': total,
                'accurate': accurate,
                'somewhat_accurate': somewhat_accurate,
                'inaccurate': inaccurate,
                'accuracy_rate': round(accuracy_rate, 2),
                'accuracy_percentage': f"{accuracy_rate:.2f}%"
            }
        
        except Exception as e:
            logger.error(f"Error getting feedback stats: {e}")
            return {}
        finally:
            cursor.close()
            conn.close()
    
    def get_feedback_by_crop(self, crop_name):
        """Get feedback for a specific crop from MySQL"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            
            query = "SELECT * FROM feedback WHERE JSON_EXTRACT(recommendation, '$.crop') = %s"
            cursor.execute(query, (crop_name,))
            feedbacks = cursor.fetchall()
            
            # Parse JSON fields
            for f in feedbacks:
                if f.get('original_input'):
                    f['original_input'] = json.loads(f['original_input'])
                if f.get('recommendation'):
                    f['recommendation'] = json.loads(f['recommendation'])
            
            return feedbacks
        
        except Exception as e:
            logger.error(f"Error getting crop feedback from MySQL: {e}")
            return []
        finally:
            cursor.close()
            conn.close()
    
    def get_crop_accuracy(self, crop_name):
        """Calculate accuracy rate for a specific crop"""
        crop_feedbacks = self.get_feedback_by_crop(crop_name)
        
        if not crop_feedbacks:
            return {
                'crop': crop_name,
                'total_recommendations': 0,
                'accuracy_rate': 0
            }
        
        accurate_count = sum(
            1 for f in crop_feedbacks 
            if f.get('accuracy') in ['accurate', 'somewhat_accurate']
        )
        
        accuracy_rate = (accurate_count / len(crop_feedbacks)) * 100
        
        return {
            'crop': crop_name,
            'total_recommendations': len(crop_feedbacks),
            'accurate': accurate_count,
            'accuracy_rate': round(accuracy_rate, 2)
        }
    
    def delete_feedback(self, feedback_id):
        """Delete a specific feedback entry"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM feedback WHERE id = %s", (feedback_id,))
            conn.commit()
            logger.info(f"Feedback {feedback_id} deleted")
            return True
        except Exception as e:
            logger.error(f"Error deleting feedback: {e}")
            return False
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            try:
                conn.close()
            except Exception:
                pass
            return False
