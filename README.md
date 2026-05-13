# AgriCrop - Crop Recommendation Expert System

A modern web-based Expert System that provides high-accuracy crop recommendations using AI, machine learning, and expert system logic.

##  Overview

AgriCrop helps farmers and agricultural professionals make data-driven decisions by analyzing soil nutrients (N, P, K), environmental factors (temperature, humidity, rainfall), and soil quality (pH) to recommend the most suitable crops for their specific conditions.

###  Key Features

- **AI-Powered Analysis**: Forward Chaining inference engine with ML classification
- **Machine Learning**: Naive Bayes and Decision Tree ensemble models
- **Smart Preprocessing**: Automatic unit conversion and input validation
- **Modern UI**: Beautiful, responsive interface with agricultural theme
- **Confidence Scoring**: Statistical probability metrics for recommendations
- **User Accounts**: Authentication, profiles, and recommendation history
- **Feedback System**: Continuous improvement through user feedback
- **20+ Crops**: Comprehensive database with detailed growing conditions

##  System Architecture

### Backend Modules

- **Knowledge Base**: Ideal growing conditions for 20+ crops
- **Data Preprocessor**: Input validation, unit conversion, normalization
- **Inference Engine**: Forward Chaining algorithm with confidence scoring
- **Classification Model**: Naive Bayes + Decision Tree ensemble
- **Feedback Manager**: User feedback collection and analysis
- **Auth Manager**: User authentication and session management
- **History Manager**: Recommendation history tracking

### Frontend Components

- **Landing Page**: Modern hero section with agricultural imagery
- **Dashboard**: Intuitive input form for soil/environmental parameters
- **Output Page**: Beautiful recommendation display with confidence meters
- **Profile Page**: User account management and history
- **Responsive Design**: Mobile-friendly across all devices

##  Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to project directory**
   ```bash
   cd "c:\Users\lenovo\OneDrive\Desktop\Agri cul"
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
  
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python backend/app.py
   ```

5. **Access the application**
   - Open browser: `http://localhost:8080`

##  Project Structure

```
Agri cul - Copy/
├── backend/
│   ├── app.py              # Main Flask application
│   └── modules/
│       ├── knowledge_base.py
│       ├── data_preprocessor.py
│       ├── inference_engine.py
│       ├── classifier.py
│       ├── feedback_manager.py
│       ├── auth_manager.py
│       └── history_manager.py
├── frontend/
│   ├── templates/
│   │   ├── index.html      # Landing page
│   │   ├── dashboard.html  # Input form
│   │   ├── output.html     # Results page
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── profile.html
│   │   └── about.html
│   └── static/
│       ├── css/style.css
│       ├── js/main.js
│       └── js/output.js
├── tests/                  # Test suite
├── requirements.txt
├── .env                    # Environment variables
└── README.md
```

##  API Endpoints

### POST /api/recommend
Get crop recommendation based on soil and environmental parameters.

### POST /api/feedback
Submit feedback on recommendations.

### GET /api/crops
Get list of all available crops.

### GET /api/crop/<crop_name>
Get detailed information about a specific crop.

##  Supported Crops

Rice, Wheat, Corn, Soybean, Cotton, Sugarcane, Potato, Tomato, Onion, Garlic, Cabbage, Carrots, Banana, Mango, Apple, Pumpkin, Cucumber, Lettuce, Chili, Peas

## 🎨 Design System

- **Primary Color**: Green (#2ecc71) - representing agriculture and growth
- **Secondary Color**: Blue (#3498db) - representing trust and technology
- **Accent Colors**: Orange (#f39c12), Red (#e74c3c)
- **Typography**: Segoe UI, clean and modern
- **Design**: Modern, responsive, with smooth animations

## 📝 Academic Compliance

This project implements:
- **Unit 8.6**: Knowledge Base with structured crop database
- **Unit 8.7**: Inference Engine with Forward Chaining
- **Unit 5**: Classification Models (Naive Bayes, Decision Tree)
- **Unit 2**: Data Preprocessing and validation
- **Unit 7.2**: Statistical reasoning and confidence scoring
- **Unit 6**: Cluster analysis for alternative suggestions

## 🔧 Configuration

Environment variables in `.env`:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DEBUG=True
```

## 🐛 Troubleshooting

**Port already in use**: Change port in `backend/app.py` (line 435)

**Module not found**: Run `pip install -r requirements.txt`

**Images not loading**: Ensure images are in `frontend/static/images/`

## 📄 License

This project is part of academic coursework for BIT355CO.

---

**Version**: 2.0  
**Last Updated**: May 11, 2026  
**Status**: Production Ready 
