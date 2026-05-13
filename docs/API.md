# API Documentation
## Crop Recommendation Expert System

**Base URL**: `http://localhost:5000`

---

## Endpoints Overview

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/recommend` | Get crop recommendation |
| POST | `/api/feedback` | Submit feedback on recommendation |
| GET | `/api/crops` | Get list of all crops |
| GET | `/api/crop/<name>` | Get details of specific crop |
| GET | `/health` | System health check |

---

## 1. POST /api/recommend

Get a crop recommendation based on soil and environmental parameters.

### Request

**Content-Type**: `application/json`

**Request Body**:
```json
{
    "nitrogen": 50,
    "phosphorus": 25,
    "potassium": 45,
    "temperature": 25,
    "temperature_unit": "C",
    "humidity": 80,
    "rainfall": 1200,
    "ph": 6.5,
    "season": "Monsoon",
    "location": "Kerala"
}
```

### Parameters

| Parameter | Type | Unit | Range | Required | Description |
|-----------|------|------|-------|----------|-------------|
| nitrogen | number | mg/kg | 0-250 | Yes | Nitrogen level in soil |
| phosphorus | number | mg/kg | 0-150 | Yes | Phosphorus level in soil |
| potassium | number | mg/kg | 0-200 | Yes | Potassium level in soil |
| temperature | number | varies | -10 to 50 | Yes | Ambient temperature |
| temperature_unit | string | - | C/F/K | No | Temperature unit (default: C) |
| humidity | number | % | 0-100 | Yes | Relative humidity |
| rainfall | number | mm | 0-5000 | Yes | Annual/seasonal rainfall |
| ph | number | pH | 0-14 | Yes | Soil pH value |
| season | string | - | - | No | Season (Summer/Monsoon/Winter/Spring) |
| location | string | - | - | No | Geographic location |

### Response (Success)

**Status**: `200 OK`

```json
{
    "primary_crop": "Rice",
    "confidence": 85.5,
    "alternatives": [
        {
            "crop": "Sugarcane",
            "confidence": 72.3
        },
        {
            "crop": "Corn",
            "confidence": 68.1
        }
    ],
    "reasoning": "This crop is recommended based on your soil nutrients and environmental conditions. Rice is well-suited for Monsoon season.",
    "seasonal_note": "Your area receives adequate rainfall for rice cultivation."
}
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| primary_crop | string | Name of recommended crop |
| confidence | number | Confidence score 0-100% |
| alternatives | array | List of alternative crops |
| alternatives[].crop | string | Alternative crop name |
| alternatives[].confidence | number | Alternative confidence score |
| reasoning | string | Explanation of recommendation |
| seasonal_note | string | Seasonal or environmental notes |

### Error Response

**Status**: `400 Bad Request`

```json
{
    "error": "nitrogen out of range. Expected 0-250, got 300"
}
```

### Example Request (cURL)

```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{
    "nitrogen": 50,
    "phosphorus": 25,
    "potassium": 45,
    "temperature": 25,
    "temperature_unit": "C",
    "humidity": 80,
    "rainfall": 1200,
    "ph": 6.5,
    "season": "Monsoon"
  }'
```

### Example Request (JavaScript)

```javascript
const data = {
    nitrogen: 50,
    phosphorus: 25,
    potassium: 45,
    temperature: 25,
    temperature_unit: "C",
    humidity: 80,
    rainfall: 1200,
    ph: 6.5,
    season: "Monsoon"
};

fetch('/api/recommend', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(data)
})
.then(response => response.json())
.then(data => console.log('Recommendation:', data))
.catch(error => console.error('Error:', error));
```

---

## 2. POST /api/feedback

Submit user feedback about recommendation accuracy.

### Request

**Content-Type**: `application/json`

**Request Body**:
```json
{
    "original_input": {
        "nitrogen": 50,
        "phosphorus": 25,
        "potassium": 45,
        "temperature": 25,
        "humidity": 80,
        "rainfall": 1200,
        "ph": 6.5
    },
    "recommendation": {
        "crop": "Rice",
        "confidence": 85.5
    },
    "accuracy": "accurate",
    "comment": "Great recommendation! Rice grew well.",
    "actual_crop": "Rice"
}
```

### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| original_input | object | Yes | Original input parameters for recommendation |
| recommendation | object | Yes | Recommendation that was provided |
| accuracy | string | Yes | 'accurate', 'somewhat_accurate', or 'inaccurate' |
| comment | string | No | Optional user comment |
| actual_crop | string | No | What crop user actually planted |

### Response (Success)

**Status**: `200 OK`

```json
{
    "message": "Feedback recorded successfully"
}
```

### Error Response

**Status**: `400 Bad Request`

```json
{
    "error": "Invalid accuracy value"
}
```

### Example Request (JavaScript)

```javascript
const feedbackData = {
    original_input: {
        nitrogen: 50,
        phosphorus: 25,
        potassium: 45,
        temperature: 25,
        humidity: 80,
        rainfall: 1200,
        ph: 6.5
    },
    recommendation: {
        crop: "Rice",
        confidence: 85.5
    },
    accuracy: "accurate",
    comment: "Rice performed excellently!",
    actual_crop: "Rice"
};

fetch('/api/feedback', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json'
    },
    body: JSON.stringify(feedbackData)
})
.then(response => response.json())
.then(data => console.log('Feedback submitted:', data))
.catch(error => console.error('Error:', error));
```

---

## 3. GET /api/crops

Get list of all available crops.

### Request

```
GET /api/crops
```

### Response (Success)

**Status**: `200 OK`

```json
[
    {
        "name": "Rice",
        "image": "rice.jpg",
        "description": "Staple grain crop requiring warm temperatures and adequate water"
    },
    {
        "name": "Wheat",
        "image": "wheat.jpg",
        "description": "Winter crop with moderate water and nutrient requirements"
    },
    ...
]
```

### Example Request (JavaScript)

```javascript
fetch('/api/crops')
    .then(response => response.json())
    .then(crops => {
        console.log(`Available crops: ${crops.length}`);
        crops.forEach(crop => console.log(crop.name));
    });
```

---

## 4. GET /api/crop/<crop_name>

Get detailed information about a specific crop.

### Request

```
GET /api/crop/Rice
```

### Response (Success)

**Status**: `200 OK`

```json
{
    "name": "Rice",
    "image": "rice.jpg",
    "nitrogen": {
        "min": 20,
        "max": 100
    },
    "phosphorus": {
        "min": 10,
        "max": 50
    },
    "potassium": {
        "min": 30,
        "max": 60
    },
    "ph": {
        "min": 5.0,
        "max": 7.0
    },
    "temperature": {
        "min": 20,
        "max": 35
    },
    "humidity": {
        "min": 60,
        "max": 100
    },
    "rainfall": {
        "min": 600,
        "max": 2000
    },
    "description": "Staple grain crop requiring warm temperatures and adequate water",
    "season": ["Monsoon", "Summer"]
}
```

### Error Response

**Status**: `404 Not Found`

```json
{
    "error": "Crop not found"
}
```

### Example Request (JavaScript)

```javascript
fetch('/api/crop/Rice')
    .then(response => response.json())
    .then(crop => {
        console.log(`${crop.name} requires:`);
        console.log(`- Nitrogen: ${crop.nitrogen.min}-${crop.nitrogen.max} mg/kg`);
        console.log(`- Temperature: ${crop.temperature.min}-${crop.temperature.max}°C`);
    });
```

---

## 5. GET /health

System health check endpoint.

### Request

```
GET /health
```

### Response

**Status**: `200 OK`

```json
{
    "status": "ok",
    "message": "Expert System is running"
}
```

### Example Request (JavaScript)

```javascript
fetch('/health')
    .then(response => response.json())
    .then(data => console.log('System status:', data.status));
```

---

## Error Handling

### Common Error Responses

#### 400 Bad Request
```json
{
    "error": "Invalid input data: nitrogen out of range"
}
```

#### 404 Not Found
```json
{
    "error": "Crop not found"
}
```

#### 500 Internal Server Error
```json
{
    "error": "An unexpected error occurred"
}
```

---

## Rate Limiting & Best Practices

### Recommendations

1. **Batch Requests**: Avoid sending requests in rapid succession
2. **Error Handling**: Implement retry logic for transient failures
3. **Caching**: Cache crop list since it rarely changes
4. **User Feedback**: Always collect feedback for model improvement

---

## Data Validation Examples

### Valid Nitrogen Values
```javascript
// Valid: 0-250 mg/kg
nitrogen: 50   // ✓ VALID
nitrogen: 0    // ✓ VALID
nitrogen: 250  // ✓ VALID

// Invalid
nitrogen: 300  // ✗ INVALID (exceeds max)
nitrogen: -10  // ✗ INVALID (below min)
nitrogen: "50" // ✗ INVALID (must be number)
```

### Temperature Unit Conversions
```javascript
// All equivalent to 25°C
temperature: 25, temperature_unit: "C"      // Celsius
temperature: 77, temperature_unit: "F"      // Fahrenheit → 25°C
temperature: 298.15, temperature_unit: "K"  // Kelvin → 25°C
```

---

## Testing the API

### Using Postman

1. Create new POST request
2. URL: `http://localhost:5000/api/recommend`
3. Set header: `Content-Type: application/json`
4. Body (raw JSON):
```json
{
    "nitrogen": 50,
    "phosphorus": 25,
    "potassium": 45,
    "temperature": 25,
    "temperature_unit": "C",
    "humidity": 80,
    "rainfall": 1200,
    "ph": 6.5,
    "season": "Monsoon"
}
```
5. Click Send

### Using Python Requests

```python
import requests
import json

url = "http://localhost:5000/api/recommend"
data = {
    "nitrogen": 50,
    "phosphorus": 25,
    "potassium": 45,
    "temperature": 25,
    "temperature_unit": "C",
    "humidity": 80,
    "rainfall": 1200,
    "ph": 6.5,
    "season": "Monsoon"
}

response = requests.post(url, json=data)
print(response.json())
```

---

## API Rate Limits

Currently, no rate limiting is implemented. In production:
- Implement rate limiting (e.g., 100 requests/minute)
- Use API keys for tracking and authentication
- Monitor usage patterns

---

## Versioning

**Current API Version**: 1.0

Future versions may be available at `/api/v2/...` (when needed)

---

## Support

For API issues or questions:
1. Check this documentation
2. Review error messages carefully
3. Test with sample data provided
4. Check application logs for detailed errors

---

**Last Updated**: May 5, 2026
