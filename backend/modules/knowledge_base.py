"""
Knowledge Base Module (Unit 8.6)
Structured database containing ideal growth conditions for 20+ crops
"""
import json
import os

class KnowledgeBase:
    """
    Knowledge Base containing rules and ranges for crop growing conditions
    """
    
    def __init__(self):
        """Initialize knowledge base with crop data"""
        self.crops_data = self._initialize_crops()
    
    def _initialize_crops(self):
        """Initialize 20 different crops with their ideal growth conditions"""
        return {
            'Rice': {
                'name': 'Rice',
                'image': '/Images/Rice.jpg',
                'nitrogen': {'min': 20, 'max': 100},
                'phosphorus': {'min': 10, 'max': 50},
                'potassium': {'min': 30, 'max': 60},
                'ph': {'min': 5.0, 'max': 7.0},
                'temperature': {'min': 20, 'max': 35},
                'humidity': {'min': 60, 'max': 100},
                'rainfall': {'min': 600, 'max': 2000},
                'description': 'Staple grain crop requiring warm temperatures and adequate water',
                'season': ['Monsoon', 'Summer']
            },
            'Wheat': {
                'name': 'Wheat',
                'image': '/Images/Wheat.jpg',
                'nitrogen': {'min': 40, 'max': 120},
                'phosphorus': {'min': 15, 'max': 50},
                'potassium': {'min': 20, 'max': 40},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 15, 'max': 25},
                'humidity': {'min': 40, 'max': 70},
                'rainfall': {'min': 300, 'max': 600},
                'description': 'Winter crop with moderate water and nutrient requirements',
                'season': ['Winter']
            },
            'Corn': {
                'name': 'Corn',
                'image': '/Images/corn.jpg',
                'nitrogen': {'min': 60, 'max': 150},
                'phosphorus': {'min': 20, 'max': 60},
                'potassium': {'min': 30, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 18, 'max': 30},
                'humidity': {'min': 50, 'max': 80},
                'rainfall': {'min': 500, 'max': 1200},
                'description': 'High-nutrient demanding crop, suitable for warm season',
                'season': ['Summer', 'Monsoon']
            },
            'Soybean': {
                'name': 'Soybean',
                'image': '/Images/Soybean.jpg',
                'nitrogen': {'min': 0, 'max': 40},
                'phosphorus': {'min': 15, 'max': 45},
                'potassium': {'min': 20, 'max': 50},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 20, 'max': 30},
                'humidity': {'min': 50, 'max': 75},
                'rainfall': {'min': 450, 'max': 900},
                'description': 'Legume crop that fixes nitrogen, requires warm temperatures',
                'season': ['Summer', 'Monsoon']
            },
            'Cotton': {
                'name': 'Cotton',
                'image': '/Images/Cotton.jpg',
                'nitrogen': {'min': 50, 'max': 100},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 21, 'max': 32},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 500, 'max': 1200},
                'description': 'Cash crop requiring warm climate and moderate moisture',
                'season': ['Summer']
            },
            'Sugarcane': {
                'name': 'Sugarcane',
                'image': '/Images/Sugarcane.jpg',
                'nitrogen': {'min': 100, 'max': 200},
                'phosphorus': {'min': 40, 'max': 80},
                'potassium': {'min': 60, 'max': 120},
                'ph': {'min': 5.5, 'max': 7.0},
                'temperature': {'min': 20, 'max': 30},
                'humidity': {'min': 70, 'max': 90},
                'rainfall': {'min': 750, 'max': 2000},
                'description': 'High-nutrient demanding cash crop requiring ample moisture',
                'season': ['Monsoon', 'Summer']
            },
            'Potato': {
                'name': 'Potato',
                'image': '/Images/Potato.jpg',
                'nitrogen': {'min': 80, 'max': 150},
                'phosphorus': {'min': 40, 'max': 80},
                'potassium': {'min': 60, 'max': 100},
                'ph': {'min': 5.5, 'max': 7.5},
                'temperature': {'min': 10, 'max': 20},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 400, 'max': 700},
                'description': 'Cool season tuber crop with moderate nutrient needs',
                'season': ['Winter']
            },
            'Tomato': {
                'name': 'Tomato',
                'image': '/Images/Tomato.jpg',
                'nitrogen': {'min': 40, 'max': 100},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 30, 'max': 70},
                'ph': {'min': 6.0, 'max': 6.8},
                'temperature': {'min': 20, 'max': 28},
                'humidity': {'min': 50, 'max': 80},
                'rainfall': {'min': 400, 'max': 800},
                'description': 'Vegetable crop requiring warm temperatures and moderate nutrients',
                'season': ['Summer', 'Monsoon']
            },
            'Onion': {
                'name': 'Onion',
                'image': '/Images/Onion.jpg',
                'nitrogen': {'min': 60, 'max': 120},
                'phosphorus': {'min': 30, 'max': 60},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 15, 'max': 25},
                'humidity': {'min': 40, 'max': 60},
                'rainfall': {'min': 300, 'max': 600},
                'description': 'Bulb crop suitable for cool seasons with moderate water needs',
                'season': ['Winter']
            },
            'Garlic': {
                'name': 'Garlic',
                'image': '/Images/Garlic.jpg',
                'nitrogen': {'min': 60, 'max': 120},
                'phosphorus': {'min': 30, 'max': 60},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 10, 'max': 20},
                'humidity': {'min': 40, 'max': 60},
                'rainfall': {'min': 300, 'max': 600},
                'description': 'Winter crop bulb with moderate nutrient requirements',
                'season': ['Winter']
            },
            'Cabbage': {
                'name': 'Cabbage',
                'image': '/Images/Cabbage.jpg',
                'nitrogen': {'min': 60, 'max': 120},
                'phosphorus': {'min': 30, 'max': 60},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 15, 'max': 25},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 400, 'max': 700},
                'description': 'Cool season leafy vegetable requiring moderate nutrients',
                'season': ['Winter']
            },
            'Carrots': {
                'name': 'Carrots',
                'image': '/Images/Carrots.jpg',
                'nitrogen': {'min': 40, 'max': 80},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 30, 'max': 60},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 15, 'max': 25},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 400, 'max': 700},
                'description': 'Root vegetable crop for cool seasons',
                'season': ['Winter']
            },
            'Banana': {
                'name': 'Banana',
                'image': '/Images/Banana.jpg',
                'nitrogen': {'min': 80, 'max': 150},
                'phosphorus': {'min': 30, 'max': 60},
                'potassium': {'min': 100, 'max': 150},
                'ph': {'min': 5.5, 'max': 7.5},
                'temperature': {'min': 20, 'max': 35},
                'humidity': {'min': 70, 'max': 90},
                'rainfall': {'min': 800, 'max': 2000},
                'description': 'Tropical fruit crop requiring high potassium and moisture',
                'season': ['Year-round']
            },
            'Mango': {
                'name': 'Mango',
                'image': '/Images/Mango.jpg',
                'nitrogen': {'min': 40, 'max': 100},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 5.5, 'max': 7.5},
                'temperature': {'min': 24, 'max': 30},
                'humidity': {'min': 60, 'max': 80},
                'rainfall': {'min': 600, 'max': 2000},
                'description': 'Tropical fruit tree requiring warm climate',
                'season': ['Summer']
            },
            'Apple': {
                'name': 'Apple',
                'image': '/Images/Apple.jpg',
                'nitrogen': {'min': 40, 'max': 100},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.0},
                'temperature': {'min': 5, 'max': 25},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 400, 'max': 800},
                'description': 'Temperate fruit tree requiring cool winters',
                'season': ['Winter']
            },
            'Pumpkin': {
                'name': 'Pumpkin',
                'image': '/Images/Pumpkin.jpg',
                'nitrogen': {'min': 40, 'max': 80},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.0},
                'temperature': {'min': 20, 'max': 30},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 400, 'max': 800},
                'description': 'Warm season cucurbit crop with moderate requirements',
                'season': ['Summer', 'Monsoon']
            },
            'Cucumber': {
                'name': 'Cucumber',
                'image': '/Images/Cucumber.jpg',
                'nitrogen': {'min': 40, 'max': 80},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 40, 'max': 80},
                'ph': {'min': 6.0, 'max': 7.0},
                'temperature': {'min': 20, 'max': 32},
                'humidity': {'min': 60, 'max': 85},
                'rainfall': {'min': 400, 'max': 800},
                'description': 'Warm season vegetable requiring adequate moisture',
                'season': ['Summer', 'Monsoon']
            },
            'Lettuce': {
                'name': 'Lettuce',
                'image': '/Images/Lettuce.jpg',
                'nitrogen': {'min': 40, 'max': 100},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 30, 'max': 60},
                'ph': {'min': 6.0, 'max': 7.0},
                'temperature': {'min': 15, 'max': 20},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 300, 'max': 600},
                'description': 'Cool season leafy green with moderate nutrients',
                'season': ['Winter']
            },
            'Chili': {
                'name': 'Chili',
                'image': '/Images/Chili.jpg',
                'nitrogen': {'min': 40, 'max': 100},
                'phosphorus': {'min': 20, 'max': 50},
                'potassium': {'min': 30, 'max': 70},
                'ph': {'min': 6.0, 'max': 6.8},
                'temperature': {'min': 20, 'max': 30},
                'humidity': {'min': 50, 'max': 80},
                'rainfall': {'min': 400, 'max': 1000},
                'description': 'Spice crop requiring warm temperatures',
                'season': ['Summer', 'Monsoon']
            },
            'Peas': {
                'name': 'Peas',
                'image': '/Images/Peas.jpg',
                'nitrogen': {'min': 0, 'max': 30},
                'phosphorus': {'min': 15, 'max': 45},
                'potassium': {'min': 20, 'max': 50},
                'ph': {'min': 6.0, 'max': 7.5},
                'temperature': {'min': 10, 'max': 18},
                'humidity': {'min': 50, 'max': 70},
                'rainfall': {'min': 300, 'max': 700},
                'description': 'Cool season legume requiring low nitrogen',
                'season': ['Winter']
            }
        }
    
    def get_crop_info(self, crop_name):
        """Get information about a specific crop"""
        return self.crops_data.get(crop_name)
    
    def get_all_crops(self):
        """Get list of all crops"""
        crops_list = []
        for crop_name, crop_data in self.crops_data.items():
            crops_list.append({
                'name': crop_name,
                'image': crop_data['image'],
                'description': crop_data['description']
            })
        return crops_list
    
    def check_rule_match(self, params):
        """
        Forward Chaining: Check if parameters match "Golden Rules"
        Returns matching crops with confidence scores
        """
        matches = []
        
        for crop_name, crop_data in self.crops_data.items():
            score = 0
            max_score = 5  # N, P, K, pH, Temperature
            
            # Check nitrogen
            if (crop_data['nitrogen']['min'] <= params['nitrogen'] <= crop_data['nitrogen']['max']):
                score += 1
            
            # Check phosphorus
            if (crop_data['phosphorus']['min'] <= params['phosphorus'] <= crop_data['phosphorus']['max']):
                score += 1
            
            # Check potassium
            if (crop_data['potassium']['min'] <= params['potassium'] <= crop_data['potassium']['max']):
                score += 1
            
            # Check pH
            if (crop_data['ph']['min'] <= params['ph'] <= crop_data['ph']['max']):
                score += 1
            
            # Check temperature
            if (crop_data['temperature']['min'] <= params['temperature'] <= crop_data['temperature']['max']):
                score += 1
            
            confidence = score / max_score
            
            if confidence >= 0.7:  # 70% match threshold for rule-based recommendation
                matches.append({
                    'crop': crop_name,
                    'confidence': confidence,
                    'data': crop_data
                })
        
        # Sort by confidence
        matches.sort(key=lambda x: x['confidence'], reverse=True)
        return matches
    
    def get_seasonal_crops(self, season):
        """Get crops suitable for a specific season"""
        seasonal_crops = []
        for crop_name, crop_data in self.crops_data.items():
            if season in crop_data['season']:
                seasonal_crops.append(crop_name)
        return seasonal_crops
