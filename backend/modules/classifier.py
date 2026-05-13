"""
Classification Model Module (Unit 5)
Implements Naive Bayes and Decision Tree for ML-based crop prediction
"""
import logging
import numpy as np
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
import pickle
import os

logger = logging.getLogger(__name__)


class CropClassifier:
    """
    Machine Learning Classifier for Crop Prediction
    Uses both Naive Bayes and Decision Tree models
    """
    
    def __init__(self):
        """Initialize classifier with trained models"""
        self.naive_bayes_model = None
        self.decision_tree_model = None
        self.scaler = StandardScaler()
        self.crop_labels = []
        self.is_trained = False
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize with default models or load from saved state"""
        try:
            # Try to load pre-trained models
            model_path = os.path.join(
                os.path.dirname(__file__), 
                '..', 'data', 'trained_models'
            )
            if os.path.exists(os.path.join(model_path, 'nb_model.pkl')):
                self._load_models(model_path)
            else:
                # Initialize with dummy training if no saved models
                self._train_default_models()
        except Exception as e:
            logger.warning(f"Could not load models: {e}, using default")
            self._train_default_models()
    
    def _train_default_models(self):
        """
        Train models with synthetic data representing crop conditions
        """
        logger.info("Training models with synthetic data")
        
        # Synthetic training data: [N, P, K, pH, Temp, Humidity, Rainfall]
        X_train = np.array([
            # Rice conditions (high rainfall, moderate N, P, K, temp 20-35)
            [50, 25, 45, 6.5, 25, 80, 1200],
            [60, 30, 40, 6.0, 28, 85, 1500],
            [45, 20, 50, 6.8, 23, 75, 1000],
            # Wheat conditions (moderate N, low rainfall, temp 15-25)
            [80, 30, 30, 6.5, 18, 55, 400],
            [100, 40, 25, 6.8, 20, 50, 350],
            [70, 25, 35, 6.0, 15, 60, 500],
            # Corn conditions (high N, temp 18-30)
            [120, 40, 60, 6.5, 25, 65, 800],
            [100, 35, 50, 6.0, 22, 60, 900],
            [150, 50, 70, 7.0, 28, 70, 750],
            # Potato conditions (high N, cool temp, moderate rainfall)
            [120, 60, 90, 6.5, 15, 60, 500],
            [100, 50, 80, 6.0, 12, 55, 550],
            [130, 70, 100, 7.0, 18, 65, 450],
            # Sugarcane (very high N, high rainfall, warm)
            [180, 60, 100, 6.0, 25, 80, 1500],
            [200, 70, 120, 6.5, 28, 85, 1800],
            [160, 50, 90, 5.8, 26, 75, 1200],
            # Additional crops for diversity
            [60, 25, 50, 6.5, 22, 70, 600],  # Generic vegetable
            [40, 20, 40, 6.0, 20, 60, 400],  # Generic legume
            [90, 35, 70, 6.5, 25, 75, 1000], # Generic fruit
            [110, 40, 60, 6.8, 26, 70, 800], # Generic grain
            [70, 30, 55, 6.2, 23, 65, 700],  # Mixed crop
        ])
        
        # Labels: 0=Rice, 1=Wheat, 2=Corn, 3=Potato, 4=Sugarcane, 5-9=Others
        y_train = np.array([0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4, 4, 4, 5, 6, 7, 8, 9])
        
        self.crop_labels = ['Rice', 'Wheat', 'Corn', 'Potato', 'Sugarcane', 
                           'Cotton', 'Soybean', 'Tomato', 'Onion', 'Cabbage']
        
        # Scale the data
        X_scaled = self.scaler.fit_transform(X_train)
        
        # Train Naive Bayes
        self.naive_bayes_model = GaussianNB()
        self.naive_bayes_model.fit(X_scaled, y_train)
        logger.info("Naive Bayes model trained")
        
        # Train Decision Tree
        self.decision_tree_model = DecisionTreeClassifier(max_depth=5, random_state=42)
        self.decision_tree_model.fit(X_scaled, y_train)
        logger.info("Decision Tree model trained")
        
        self.is_trained = True
    
    def predict(self, user_params):
        """
        Predict crop recommendation using ML models
        Uses ensemble method with Naive Bayes and Decision Tree
        """
        if not self.is_trained:
            logger.warning("Models not trained, initializing...")
            self._train_default_models()
        
        # Extract features in order: [N, P, K, pH, Temp, Humidity, Rainfall]
        features = np.array([
            user_params['nitrogen'],
            user_params['phosphorus'],
            user_params['potassium'],
            user_params['ph'],
            user_params['temperature'],
            user_params['humidity'],
            user_params['rainfall']
        ]).reshape(1, -1)
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get predictions from both models
        nb_pred = self.naive_bayes_model.predict(features_scaled)[0]
        dt_pred = self.decision_tree_model.predict(features_scaled)[0]
        
        # Get probabilities
        nb_proba = self.naive_bayes_model.predict_proba(features_scaled)[0]
        dt_proba = self.decision_tree_model.predict_proba(features_scaled)[0]
        
        # Ensemble: Average probabilities
        ensemble_proba = (nb_proba + dt_proba) / 2
        best_idx = np.argmax(ensemble_proba)
        confidence = ensemble_proba[best_idx]
        
        primary_crop = self.crop_labels[best_idx]
        
        # Get top 3 alternative predictions
        top_indices = np.argsort(ensemble_proba)[-3:][::-1]
        alternatives = []
        for idx in top_indices[1:]:  # Skip first (primary)
            alternatives.append({
                'crop': self.crop_labels[idx],
                'confidence': round(ensemble_proba[idx] * 100, 2)
            })
        
        logger.info(f"ML Prediction: {primary_crop} with confidence {confidence:.2%}")
        
        return {
            'primary_crop': primary_crop,
            'confidence': confidence,
            'alternatives': alternatives,
            'method': 'ml-ensemble'
        }
    
    def _load_models(self, model_path):
        """Load pre-trained models"""
        try:
            with open(os.path.join(model_path, 'nb_model.pkl'), 'rb') as f:
                self.naive_bayes_model = pickle.load(f)
            with open(os.path.join(model_path, 'dt_model.pkl'), 'rb') as f:
                self.decision_tree_model = pickle.load(f)
            with open(os.path.join(model_path, 'scaler.pkl'), 'rb') as f:
                self.scaler = pickle.load(f)
            self.is_trained = True
            logger.info("Models loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load models: {e}")
            raise
    
    def save_models(self, model_path):
        """Save trained models"""
        os.makedirs(model_path, exist_ok=True)
        try:
            with open(os.path.join(model_path, 'nb_model.pkl'), 'wb') as f:
                pickle.dump(self.naive_bayes_model, f)
            with open(os.path.join(model_path, 'dt_model.pkl'), 'wb') as f:
                pickle.dump(self.decision_tree_model, f)
            with open(os.path.join(model_path, 'scaler.pkl'), 'wb') as f:
                pickle.dump(self.scaler, f)
            logger.info("Models saved successfully")
        except Exception as e:
            logger.error(f"Failed to save models: {e}")
            raise
