"""
Inference Engine Module (Unit 8.7)
Implements Forward Chaining to match user inputs against Knowledge Base
"""
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class InferenceEngine:
    """
    Forward Chaining Inference Engine
    Matches user inputs against knowledge base rules
    """
    
    def __init__(self, knowledge_base):
        """Initialize with knowledge base"""
        self.kb = knowledge_base
        self.inference_log = []
    
    def forward_chain(self, user_params):
        """
        Forward Chaining Algorithm:
        1. Start with user facts (parameters)
        2. Match against rules in knowledge base
        3. Derive conclusions (crop recommendations)
        
        Returns: Best matching crop or None if no strong match
        """
        logger.info("Starting Forward Chaining inference")
        
        # Get all rule matches
        matches = self.kb.check_rule_match(user_params)
        
        if not matches:
            logger.info("No rule matches found")
            return None
        
        # Get best match
        best_match = matches[0]
        
        if best_match['confidence'] >= 0.8:
            # Strong confidence match
            logger.info(f"Strong match found: {best_match['crop']} (confidence: {best_match['confidence']})")
            
            # Get alternatives
            alternatives = []
            for match in matches[1:4]:  # Next 3 alternatives
                alternatives.append({
                    'crop': match['crop'],
                    'confidence': round(match['confidence'] * 100, 2)
                })
            
            result = {
                'crop': best_match['crop'],
                'primary_crop': best_match['crop'],
                'confidence': best_match['confidence'],
                'alternatives': alternatives,
                'method': 'rule-based'
            }
            
            self._log_inference(result)
            return result
        else:
            logger.info(f"Weak rule match: {best_match['crop']} (confidence: {best_match['confidence']})")
            return None
    
    def refine_recommendation(self, crop_name, user_params):
        """
        Step 4: Refinement with seasonal and environmental adjustments
        """
        logger.info(f"Refining recommendation for {crop_name}")
        
        crop_info = self.kb.get_crop_info(crop_name)
        if not crop_info:
            return {'reasoning': 'Crop not found', 'seasonal_note': ''}
        
        reasoning = f"This crop is recommended based on your soil nutrients and environmental conditions."
        seasonal_note = ""
        
        # Check seasonal suitability
        season = user_params.get('season', 'Summer')
        if season in crop_info.get('season', []):
            reasoning += f" {crop_name} is well-suited for {season}."
        else:
            reasoning += f" Note: {crop_name} is typically grown in {', '.join(crop_info.get('season', []))}, but can be adapted."
        
        # Check rainfall patterns
        rainfall = user_params.get('rainfall', 0)
        if rainfall < crop_info['rainfall']['min']:
            seasonal_note += "Your area receives less rainfall than ideal. Consider irrigation."
        elif rainfall > crop_info['rainfall']['max']:
            seasonal_note += "Your area receives more rainfall than typical. Ensure proper drainage."
        
        # Check temperature suitability
        temperature = user_params.get('temperature', 0)
        if temperature < crop_info['temperature']['min']:
            seasonal_note += f" Temperatures are cooler than ideal for {crop_name}."
        elif temperature > crop_info['temperature']['max']:
            seasonal_note += f" Temperatures are warmer than typical for {crop_name}."
        
        return {
            'reasoning': reasoning,
            'seasonal_note': seasonal_note,
            'crop_description': crop_info['description']
        }
    
    def _log_inference(self, result):
        """Log inference step for debugging"""
        self.inference_log.append({
            'timestamp': datetime.now().isoformat(),
            'result': result
        })
    
    def get_inference_log(self):
        """Return inference log"""
        return self.inference_log
    
    def reset_log(self):
        """Clear inference log"""
        self.inference_log = []
