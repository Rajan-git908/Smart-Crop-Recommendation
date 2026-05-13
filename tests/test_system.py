"""
Test cases for crop recommendation system
Quick test script to verify system functionality
"""

import json
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from modules.knowledge_base import KnowledgeBase
from modules.data_preprocessor import DataPreprocessor
from modules.inference_engine import InferenceEngine
from modules.classifier import CropClassifier


def test_knowledge_base():
    """Test Knowledge Base"""
    print("\n=== Testing Knowledge Base ===")
    kb = KnowledgeBase()
    
    # Test crop retrieval
    crops = kb.get_all_crops()
    print(f"✓ Found {len(crops)} crops")
    assert len(crops) == 20, "Should have 20 crops"
    
    # Test specific crop
    rice = kb.get_crop_info('Rice')
    assert rice is not None, "Rice crop not found"
    print(f"✓ Rice crop info: {rice['description']}")
    
    # Test rule matching
    test_params = {
        'nitrogen': 50,
        'phosphorus': 25,
        'potassium': 45,
        'ph': 6.5,
        'temperature': 25
    }
    matches = kb.check_rule_match(test_params)
    assert len(matches) > 0, "Should find matches"
    print(f"✓ Found {len(matches)} crop matches for test parameters")
    print(f"  Best match: {matches[0]['crop']} ({matches[0]['confidence']*100:.1f}%)")


def test_data_preprocessor():
    """Test Data Preprocessor"""
    print("\n=== Testing Data Preprocessor ===")
    preprocessor = DataPreprocessor()
    
    # Test valid input
    raw_data = {
        'nitrogen': 50,
        'phosphorus': 25,
        'potassium': 45,
        'temperature': 25,
        'temperature_unit': 'C',
        'humidity': 80,
        'rainfall': 1200,
        'ph': 6.5,
        'season': 'Monsoon'
    }
    
    processed = preprocessor.preprocess(raw_data)
    print("✓ Successfully processed valid input")
    assert processed['nitrogen'] == 50, "Nitrogen not processed correctly"
    
    # Test temperature conversion
    raw_data['temperature'] = 77
    raw_data['temperature_unit'] = 'F'
    processed = preprocessor.preprocess(raw_data)
    assert abs(processed['temperature'] - 25.0) < 0.1, "Temperature conversion failed"
    print(f"✓ Temperature conversion: 77°F → {processed['temperature']:.1f}°C")
    
    # Test validation
    try:
        raw_data['nitrogen'] = 300  # Out of range
        preprocessor.preprocess(raw_data)
        assert False, "Should have raised error for out-of-range nitrogen"
    except ValueError as e:
        print(f"✓ Validation works: {str(e)}")


def test_inference_engine():
    """Test Inference Engine"""
    print("\n=== Testing Inference Engine ===")
    kb = KnowledgeBase()
    engine = InferenceEngine(kb)
    
    # Test forward chaining
    params = {
        'nitrogen': 50,
        'phosphorus': 25,
        'potassium': 45,
        'ph': 6.5,
        'temperature': 25,
        'humidity': 80,
        'rainfall': 1200,
        'season': 'Monsoon'
    }
    
    result = engine.forward_chain(params)
    if result:
        print(f"✓ Forward chaining found: {result['crop']} ({result['confidence']*100:.1f}% confidence)")
    else:
        print("✓ Forward chaining: No exact match (will use ML)")
    
    # Test refinement
    refined = engine.refine_recommendation('Rice', params)
    print(f"✓ Recommendation refined with seasonal advice")
    print(f"  Reasoning: {refined['reasoning']}")


def test_classifier():
    """Test ML Classifier"""
    print("\n=== Testing ML Classifier ===")
    classifier = CropClassifier()
    
    params = {
        'nitrogen': 50,
        'phosphorus': 25,
        'potassium': 45,
        'ph': 6.5,
        'temperature': 25,
        'humidity': 80,
        'rainfall': 1200
    }
    
    prediction = classifier.predict(params)
    print(f"✓ ML Prediction: {prediction['primary_crop']} ({prediction['confidence']*100:.1f}% confidence)")
    alt_text = ', '.join([f"{alt['crop']} ({alt['confidence']}%)" for alt in prediction['alternatives']])
    print(f"  Alternatives: {alt_text}")


def test_end_to_end():
    """Test complete workflow"""
    print("\n=== Testing End-to-End Workflow ===")
    
    # Initialize modules
    kb = KnowledgeBase()
    preprocessor = DataPreprocessor()
    engine = InferenceEngine(kb)
    classifier = CropClassifier()
    
    # Raw input
    raw_input = {
        'nitrogen': 80,
        'phosphorus': 30,
        'potassium': 30,
        'temperature': 18,
        'temperature_unit': 'C',
        'humidity': 55,
        'rainfall': 400,
        'ph': 6.5,
        'season': 'Winter'
    }
    
    # Step 1: Preprocess
    print("Step 1: Data Preprocessing...")
    processed = preprocessor.preprocess(raw_input)
    print(f"  ✓ Data validated and normalized")
    
    # Step 2: Forward Chaining
    print("Step 2: Forward Chaining Inference...")
    rule_match = engine.forward_chain(processed)
    
    if rule_match:
        print(f"  ✓ Rule match found: {rule_match['crop']}")
        result = rule_match
    else:
        print("  → No exact rule match, using ML...")
        # Step 3: ML Classification
        print("Step 3: ML Classification...")
        result = classifier.predict(processed)
        print(f"  ✓ ML prediction: {result['primary_crop']}")
    
    # Step 4: Refinement
    print("Step 4: Recommendation Refinement...")
    refined = engine.refine_recommendation(result['primary_crop'], processed)
    print(f"  ✓ Recommendation refined")
    
    # Final output
    print("\n" + "="*50)
    print("FINAL RECOMMENDATION")
    print("="*50)
    print(f"Primary Crop: {result['primary_crop']}")
    print(f"Confidence: {result['confidence']*100:.1f}%")
    print(f"Reasoning: {refined['reasoning']}")
    if refined.get('seasonal_note'):
        print(f"Note: {refined['seasonal_note']}")
    print("="*50)


def main():
    """Run all tests"""
    print("🌾 Crop Recommendation Expert System - Test Suite")
    print("=" * 60)
    
    try:
        test_knowledge_base()
        test_data_preprocessor()
        test_inference_engine()
        test_classifier()
        test_end_to_end()
        
        print("\n" + "="*60)
        print("✅ ALL TESTS PASSED!")
        print("="*60)
        print("\nSystem is ready for use. Start with:")
        print("  python backend/app.py")
        print("\nThen open browser: http://localhost:5000")
        
    except Exception as e:
        print(f"\n❌ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
