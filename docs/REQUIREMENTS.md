# Requirements Specification
## Crop Recommendation Expert System

**Document Version**: 1.0  
**Date**: May 5, 2026  
**Project**: BIT355CO - Crop Recommendation Expert System  

---

## 1. Introduction

### 1.1 Purpose
This document specifies the functional and non-functional requirements for the Crop Recommendation Expert System, a web-based application that provides accurate crop recommendations based on soil and environmental parameters.

### 1.2 Scope
The system serves agricultural professionals, farmers, and agricultural consultants by:
- Accepting soil nutrient and environmental data
- Applying expert system logic (Forward Chaining)
- Using machine learning for predictions
- Returning ranked crop recommendations
- Collecting user feedback for continuous improvement

### 1.3 Intended Audience
- Software developers
- Quality assurance engineers
- Project managers
- Stakeholders

---

## 2. System Overview

### 2.1 System Architecture
```
Client Layer (Frontend)
    ↓
API Layer (Flask)
    ↓
Business Logic Layer (Modules)
    ↓
Data Layer (Knowledge Base + Feedback)
```

### 2.2 Key Components
1. **Frontend**: HTML5/CSS3/JavaScript responsive interface
2. **Backend**: Python Flask API server
3. **Knowledge Base**: 20 crops with growing conditions
4. **Inference Engine**: Forward Chaining algorithm
5. **Classification Model**: Naive Bayes + Decision Tree ensemble
6. **Data Preprocessor**: Input validation and normalization

---

## 3. Functional Requirements

### 3.1 User Input Handling (FR1)

**Requirement**: System shall accept the following parameters:
- Soil Nutrients (N, P, K) in mg/kg
- Environmental Factors: Temperature (°C), Humidity (%), Rainfall (mm)
- Soil Quality: pH scale (0-14)
- Seasonal information
- Location (optional)

**Acceptance Criteria**:
- ✅ All parameters can be entered via web form
- ✅ Input validation with error messages
- ✅ Range validation for each parameter
- ✅ Support for multiple temperature units (°C, °F, K)

**Priority**: HIGH

---

### 3.2 Forward Chaining Inference (FR2)

**Requirement**: System shall implement Forward Chaining algorithm to match user inputs against knowledge base rules.

**Process**:
1. Start with user facts (preprocessed parameters)
2. Match against "Golden Rules" in knowledge base
3. Calculate confidence scores for matches
4. Return best matching crops

**Acceptance Criteria**:
- ✅ Rules check all 5 parameters (N, P, K, pH, Temperature)
- ✅ Confidence threshold ≥ 70% for rule-based match
- ✅ Reasoning output explaining why crop is recommended
- ✅ Forward chaining completes in < 1 second

**Priority**: CRITICAL

---

### 3.3 Machine Learning Classification (FR3)

**Requirement**: System shall use ML classifiers when no strong rule match is found.

**Implementation**:
- Naive Bayes Classifier for probabilistic prediction
- Decision Tree for interpretable rules
- Ensemble method combining both

**Acceptance Criteria**:
- ✅ Both classifiers implemented and trainable
- ✅ Ensemble predictions combine both models
- ✅ Accuracy ≥ 75% on validation data
- ✅ Prediction completes in < 1 second

**Priority**: HIGH

---

### 3.4 Recommendation Output (FR4)

**Requirement**: System shall return ranked crop recommendations with confidence scores.

**Output Format**:
```json
{
    "primary_crop": "string",
    "confidence": number (0-100),
    "alternatives": [
        {"crop": "string", "confidence": number},
        ...
    ],
    "reasoning": "string",
    "seasonal_note": "string"
}
```

**Acceptance Criteria**:
- ✅ Primary crop is the highest confidence recommendation
- ✅ At least 2-3 alternative suggestions provided
- ✅ Confidence scores are percentages (0-100)
- ✅ Reasoning explains the recommendation
- ✅ Seasonal notes provide implementation advice

**Priority**: HIGH

---

### 3.5 Feedback Collection (FR5)

**Requirement**: System shall collect and store user feedback on recommendation accuracy.

**Feedback Types**:
- Accurate
- Somewhat Accurate
- Inaccurate

**Optional**:
- User comments
- Actual crop planted
- Additional notes

**Acceptance Criteria**:
- ✅ Feedback form on output page
- ✅ Feedback stored with timestamp
- ✅ Linked to original input parameters
- ✅ Feedback statistics accessible via API

**Priority**: MEDIUM

---

### 3.6 Crop Visualization (FR6)

**Requirement**: System shall display crop images with recommendations.

**Requirements**:
- High-quality representative images
- Crop images for all 20 crops
- Fallback/placeholder if image unavailable
- Responsive sizing

**Acceptance Criteria**:
- ✅ Primary crop displays large image
- ✅ Alternative crops show smaller images
- ✅ All crops have associated images
- ✅ Images load within 1 second
- ✅ Graceful fallback for missing images

**Priority**: MEDIUM

---

### 3.7 Data Preprocessing (FR7)

**Requirement**: System shall validate and normalize input data.

**Operations**:
- Range validation for all parameters
- Temperature unit conversion
- NPK normalization
- Data cleaning

**Acceptance Criteria**:
- ✅ Invalid inputs rejected with clear error
- ✅ Temperature conversions accurate (±0.1°C)
- ✅ Out-of-range values flagged
- ✅ Preprocessing completes in < 100ms

**Priority**: HIGH

---

## 4. Non-Functional Requirements

### 4.1 Performance (NFR1)

**Requirement**: System shall meet response time requirements.

**Metrics**:
- Total recommendation latency: < 2 seconds
- Forward Chaining: < 1 second
- ML Classification: < 1 second
- Data Preprocessing: < 100ms
- API response: < 500ms

**Acceptance Criteria**:
- ✅ 95th percentile latency < 2 seconds
- ✅ P99 latency < 3 seconds
- ✅ Average latency < 1 second

**Priority**: HIGH

---

### 4.2 Scalability (NFR2)

**Requirement**: System shall support multiple concurrent users.

**Target Capacity**:
- 100+ concurrent users
- 1000+ daily active users
- Sub-second response under load

**Acceptance Criteria**:
- ✅ Load test with 100 concurrent users
- ✅ No performance degradation under normal load
- ✅ Graceful degradation under peak load

**Priority**: MEDIUM

---

### 4.3 Availability (NFR3)

**Requirement**: System shall maintain high availability.

**Target**:
- 99% uptime (excluding maintenance)
- Automated health checks
- Error recovery

**Acceptance Criteria**:
- ✅ Health check endpoint responds < 100ms
- ✅ Graceful error handling
- ✅ Meaningful error messages to users

**Priority**: MEDIUM

---

### 4.4 Usability (NFR4)

**Requirement**: System shall provide intuitive user interface.

**Standards**:
- WCAG 2.1 AA accessibility compliance
- Mobile-responsive design
- Intuitive form layout
- Clear visual feedback

**Acceptance Criteria**:
- ✅ Works on mobile, tablet, desktop
- ✅ Form validation feedback immediate
- ✅ Loading states visible
- ✅ Error messages clear and actionable

**Priority**: HIGH

---

### 4.5 Maintainability (NFR5)

**Requirement**: Code shall be maintainable and well-documented.

**Standards**:
- PEP 8 Python style guide
- Clear module separation
- Comprehensive comments
- API documentation

**Acceptance Criteria**:
- ✅ Code passes linting checks
- ✅ Functions documented with docstrings
- ✅ README and documentation complete
- ✅ Error handling comprehensive

**Priority**: MEDIUM

---

### 4.6 Security (NFR6)

**Requirement**: System shall protect user data.

**Requirements**:
- Input validation against injection attacks
- CORS configuration
- Secure default configurations
- Error message sanitization

**Acceptance Criteria**:
- ✅ No SQL injection vulnerabilities
- ✅ Input sanitization implemented
- ✅ Sensitive data not exposed in logs
- ✅ HTTPS ready (for production)

**Priority**: HIGH

---

## 5. Data Requirements

### 5.1 Knowledge Base
**Content**: 20 crops with parameters
**Format**: In-memory JSON structure
**Fields per crop**:
- Nitrogen range (min, max) in mg/kg
- Phosphorus range (min, max) in mg/kg
- Potassium range (min, max) in mg/kg
- pH range (min, max)
- Temperature range (min, max) in °C
- Humidity range (min, max) in %
- Rainfall range (min, max) in mm
- Crop description
- Seasonal information
- Image filename

### 5.2 Training Data (ML Models)
**Source**: Synthetic agricultural data
**Format**: NumPy arrays
**Size**: 20 samples per crop (minimum)
**Features**: N, P, K, pH, Temperature, Humidity, Rainfall
**Labels**: Crop names

### 5.3 Feedback Data
**Storage**: JSON file (extensible to database)
**Fields**:
- Feedback ID
- Timestamp
- Original input parameters
- Recommendation provided
- User accuracy rating
- Optional comments
- Actual crop planted (optional)

---

## 6. Interface Requirements

### 6.1 Input Dashboard
- Clean grid-based form
- Grouped input sections (Nutrients, Environmental, Quality, Additional)
- Real-time pH slider feedback
- Clear input hints and ranges
- Submit and Reset buttons

### 6.2 Output Page
- Large primary recommendation card
- Confidence meter with percentage
- Reasoning explanation
- 2-3 alternative crops with confidence badges
- Feedback form
- Print button

### 6.3 API Interfaces
- `/api/recommend` - POST for recommendations
- `/api/feedback` - POST for feedback submission
- `/api/crops` - GET for crop list
- `/api/crop/<name>` - GET for crop details
- `/health` - GET for system health check

---

## 7. Constraints & Assumptions

### 7.1 Constraints
- Python 3.8 or higher required
- Development: Flask (production: Gunicorn/Nginx)
- Browser: Modern browsers with ES6 support
- No database requirement (can use JSON initially)

### 7.2 Assumptions
- Users have basic agricultural knowledge
- Input data is honest (no validation for geographic feasibility)
- Knowledge base represents typical Indian climate zones
- ML training data is sufficient for accuracy

---

## 8. Acceptance Criteria Summary

### Must Have (M0)
- ✅ Input form with validation
- ✅ Forward Chaining inference
- ✅ Primary crop recommendation
- ✅ Confidence scoring
- ✅ API endpoints working
- ✅ Responsive UI

### Should Have (M1)
- ✅ ML classification
- ✅ Alternative crops
- ✅ Feedback collection
- ✅ Crop images
- ✅ Reasoning output

### Nice to Have (M2)
- Database integration
- User authentication
- Advanced analytics
- Real-time weather integration
- Mobile app

---

## 9. Sign-Off

| Role | Name | Signature | Date |
|------|------|-----------|------|
| Product Owner | - | - | May 5, 2026 |
| Developer | - | - | May 5, 2026 |
| QA Lead | - | - | May 5, 2026 |

---

**Document End**
