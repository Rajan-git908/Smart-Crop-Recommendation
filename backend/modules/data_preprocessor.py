"""
Data Preprocessor Module (Unit 2)
Cleans and normalizes user inputs before analysis
"""
import logging

logger = logging.getLogger(__name__)


class DataPreprocessor:
    """
    Data Preprocessing and Normalization
    Handles unit conversions and data validation
    """
    
    def __init__(self):
        """Initialize preprocessor with validation ranges"""
        self.valid_ranges = {
            'nitrogen': {'min': 0, 'max': 250, 'unit': 'mg/kg'},
            'phosphorus': {'min': 0, 'max': 150, 'unit': 'mg/kg'},
            'potassium': {'min': 0, 'max': 200, 'unit': 'mg/kg'},
            'temperature': {'min': -10, 'max': 50, 'unit': 'Celsius'},
            'humidity': {'min': 0, 'max': 100, 'unit': '%'},
            'rainfall': {'min': 0, 'max': 5000, 'unit': 'mm'},
            'ph': {'min': 0, 'max': 14, 'unit': 'pH scale'}
        }
    
    def preprocess(self, raw_data):
        """
        Main preprocessing function
        Performs validation, normalization, and unit conversion
        """
        logger.info("Starting data preprocessing")
        
        processed_data = {}
        
        try:
            # Extract and validate each parameter
            processed_data['nitrogen'] = self._validate_numeric(
                raw_data.get('nitrogen'), 'nitrogen'
            )
            processed_data['phosphorus'] = self._validate_numeric(
                raw_data.get('phosphorus'), 'phosphorus'
            )
            processed_data['potassium'] = self._validate_numeric(
                raw_data.get('potassium'), 'potassium'
            )
            
            # Handle temperature conversion (Fahrenheit to Celsius if needed)
            temp_value = raw_data.get('temperature')
            temp_unit = raw_data.get('temperature_unit', 'C')
            processed_data['temperature'] = self._convert_temperature(temp_value, temp_unit)
            
            # Humidity validation (percentage)
            processed_data['humidity'] = self._validate_numeric(
                raw_data.get('humidity'), 'humidity'
            )
            
            # Rainfall validation
            processed_data['rainfall'] = self._validate_numeric(
                raw_data.get('rainfall'), 'rainfall'
            )
            
            # pH validation
            processed_data['ph'] = self._validate_numeric(
                raw_data.get('ph'), 'ph'
            )
            
            # Store original metadata
            processed_data['season'] = raw_data.get('season', 'Summer')
            processed_data['location'] = raw_data.get('location', '')
            
            logger.info(f"Preprocessing complete: {processed_data}")
            return processed_data
        
        except ValueError as e:
            logger.error(f"Data validation error: {str(e)}")
            raise ValueError(f"Invalid input data: {str(e)}")
    
    def _validate_numeric(self, value, param_name):
        """
        Validate numeric input within acceptable ranges
        """
        if value is None:
            raise ValueError(f"{param_name} is required")
        
        try:
            numeric_value = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"{param_name} must be a number, got {value}")
        
        valid_range = self.valid_ranges.get(param_name)
        if not valid_range:
            raise ValueError(f"Unknown parameter: {param_name}")
        
        if not (valid_range['min'] <= numeric_value <= valid_range['max']):
            raise ValueError(
                f"{param_name} out of range. Expected {valid_range['min']}-{valid_range['max']}, "
                f"got {numeric_value}"
            )
        
        return numeric_value
    
    def _convert_temperature(self, value, unit):
        """
        Convert temperature to Celsius
        Supports: C (Celsius), F (Fahrenheit), K (Kelvin)
        """
        if value is None:
            raise ValueError("temperature is required")
        
        try:
            temp_value = float(value)
        except (ValueError, TypeError):
            raise ValueError(f"temperature must be a number, got {value}")
        
        # Convert to Celsius
        if unit.upper() == 'F':
            # Fahrenheit to Celsius: (F - 32) * 5/9
            temp_celsius = (temp_value - 32) * 5/9
            logger.info(f"Converted {temp_value}°F to {temp_celsius:.2f}°C")
        elif unit.upper() == 'K':
            # Kelvin to Celsius: K - 273.15
            temp_celsius = temp_value - 273.15
            logger.info(f"Converted {temp_value}K to {temp_celsius:.2f}°C")
        elif unit.upper() == 'C':
            temp_celsius = temp_value
        else:
            raise ValueError(f"Unknown temperature unit: {unit}. Use C, F, or K")
        
        # Validate range after conversion
        if not (-10 <= temp_celsius <= 50):
            raise ValueError(
                f"temperature out of range. Expected -10 to 50°C, got {temp_celsius:.2f}°C"
            )
        
        return temp_celsius
    
    def normalize_npk(self, n, p, k):
        """
        Normalize NPK values to standard scale (0-100)
        Useful for some ML algorithms
        """
        # Calculate total and percentages
        total = n + p + k
        if total == 0:
            return {'n': 0, 'p': 0, 'k': 0}
        
        return {
            'n': (n / total) * 100,
            'p': (p / total) * 100,
            'k': (k / total) * 100
        }
    
    def get_validation_ranges(self):
        """Return validation ranges for frontend"""
        return self.valid_ranges
