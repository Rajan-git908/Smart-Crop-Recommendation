/**
 * Output Page Script
 * Displays crop recommendation and handles feedback
 */

// Crop images mapping using Unsplash
const CROP_IMAGES = {
    'Rice': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Wheat': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Corn': 'https://images.unsplash.com/photo-1551754655-a69481a924c2?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Soybean': 'https://images.unsplash.com/photo-1601493700631-2b16ec4b4716?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Cotton': 'https://images.unsplash.com/photo-1628062927219-76cd01d01f0a?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Sugarcane': 'https://images.unsplash.com/photo-1599058817765-a7aeda35f822?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Potato': 'https://images.unsplash.com/photo-1518977676601-e4eac72ab5c3?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Tomato': 'https://images.unsplash.com/photo-1592924357228-91a4daadcfea?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Onion': 'https://images.unsplash.com/photo-1618512496218-508e31686a8e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Garlic': 'https://images.unsplash.com/photo-1618512496218-508e31686a8e?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Cabbage': 'https://images.unsplash.com/photo-1594282486552-05b4d80fbb9f?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Carrots': 'https://images.unsplash.com/photo-1598170845058-32b9d7a5c376?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Banana': 'https://images.unsplash.com/photo-1603833665858-e61d17a86224?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Mango': 'https://images.unsplash.com/photo-1553279768-865429fa0078?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Apple': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Pumpkin': 'https://images.unsplash.com/photo-1604174355665-860dfcc6a8e9?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Cucumber': 'https://images.unsplash.com/photo-1587049352846-4a222e784d38?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Lettuce': 'https://images.unsplash.com/photo-1622206151226-18ca2c9ab4a1?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Chili': 'https://images.unsplash.com/photo-1565557623262-b51c2513a641?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80',
    'Peas': 'https://images.unsplash.com/photo-1587735243615-c03f25aaff15?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80'
};

document.addEventListener('DOMContentLoaded', function() {
    const loadingState = document.getElementById('loadingState');
    const resultContainer = document.getElementById('resultContainer');
    const errorState = document.getElementById('errorState');
    const errorMessageEl = document.getElementById('errorMessage');
    const feedbackForm = document.getElementById('feedbackForm');
    const feedbackMessage = document.getElementById('feedbackMessage');

    // Get recommendation from session storage or localStorage
    const recommendationData = sessionStorage.getItem('recommendation') || localStorage.getItem('recommendation');
    
    if (!recommendationData) {
        showError('No recommendation data found. Please submit a new request.');
        return;
    }

    try {
        const data = JSON.parse(recommendationData);
        console.log('Recommendation data:', data);

        // Display recommendation
        displayRecommendation(data.result, data.input);
        
        // Hide loading state
        loadingState.style.display = 'none';
        resultContainer.style.display = 'block';

        // Setup feedback form
        setupFeedbackForm(data);

    } catch (error) {
        console.error('Error processing recommendation:', error);
        showError('Error processing recommendation. Please try again.');
    }
});

function displayRecommendation(result, input) {
    // Primary crop info
    const primaryCropName = document.getElementById('primaryCropName');
    const primaryCropImage = document.getElementById('primaryCropImage');
    const primaryCropDescription = document.getElementById('primaryCropDescription');
    const confidenceFill = document.getElementById('confidenceFill');
    const confidencePercent = document.getElementById('confidencePercent');
    const reasoningText = document.getElementById('reasoningText');
    const seasonalNoteText = document.getElementById('seasonalNoteText');
    const alternativesContainer = document.getElementById('alternativesContainer');

    // Set primary crop
    const cropName = result.primary_crop;
    primaryCropName.textContent = cropName;
    primaryCropDescription.textContent = result.reasoning || 'Recommended based on your soil and environmental conditions';
    reasoningText.textContent = result.reasoning || '';
    seasonalNoteText.textContent = result.seasonal_note || '';

    // Set confidence meter
    const confidence = result.confidence;
    confidenceFill.style.width = confidence + '%';
    confidencePercent.textContent = confidence.toFixed(1) + '%';

    // Set crop image
    const imageUrl = getCropImageUrl(cropName);
    primaryCropImage.src = imageUrl;
    primaryCropImage.onerror = function() {
        this.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200"><rect fill="%23ddd" width="200" height="200"/><text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" font-size="18" fill="%23999">🌾</text></svg>';
    };

    // Display alternatives
    if (result.alternatives && result.alternatives.length > 0) {
        result.alternatives.forEach(alt => {
            const card = createAlternativeCard(alt);
            alternativesContainer.appendChild(card);
        });
    }
}

function createAlternativeCard(alternative) {
    const card = document.createElement('div');
    card.className = 'alternative-card';
    
    const imageUrl = getCropImageUrl(alternative.crop);
    
    card.innerHTML = `
        <div class="alternative-card-image">
            <img src="${imageUrl}" alt="${alternative.crop}" onerror="this.src='data:image/svg+xml,<svg xmlns=%22http://www.w3.org/2000/svg%22 viewBox=%220 0 200 200%22><rect fill=%22%23ddd%22 width=%22200%22 height=%22200%22/><text x=%2250%25%22 y=%2250%25%22 dominant-baseline=%22middle%22 text-anchor=%22middle%22 font-size=%2218%22 fill=%22%23999%22>🌾</text></svg>'">
        </div>
        <div class="alternative-card-content">
            <h4 class="alternative-crop-name">${alternative.crop}</h4>
            <div class="alternative-confidence">
                <span>Confidence:</span>
                <span class="confidence-badge">${alternative.confidence}%</span>
            </div>
        </div>
    `;
    
    return card;
}

function getCropImageUrl(cropName) {
    return CROP_IMAGES[cropName] || 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80';
}

function setupFeedbackForm(recommendationData) {
    const feedbackForm = document.getElementById('feedbackForm');
    const feedbackMessage = document.getElementById('feedbackMessage');

    feedbackForm.addEventListener('submit', async function(e) {
        e.preventDefault();

        try {
            const formData = new FormData(feedbackForm);
            const feedbackData = {
                original_input: recommendationData.input,
                recommendation: {
                    crop: recommendationData.result.primary_crop,
                    confidence: recommendationData.result.confidence
                },
                accuracy: formData.get('accuracy'),
                comment: formData.get('comment'),
                timestamp: new Date().toISOString()
            };

            console.log('Submitting feedback:', feedbackData);

            // Send feedback to backend
            const response = await fetch('/api/feedback', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(feedbackData)
            });

            if (!response.ok) {
                throw new Error('Failed to submit feedback');
            }

            // Show success message
            feedbackMessage.textContent = '✅ Thank you! Your feedback has been recorded.';
            feedbackMessage.className = 'feedback-message success';
            feedbackMessage.style.display = 'block';

            // Disable form after submission
            feedbackForm.style.opacity = '0.6';
            feedbackForm.style.pointerEvents = 'none';

            // Hide message after 5 seconds
            setTimeout(() => {
                feedbackMessage.style.display = 'none';
            }, 5000);

        } catch (error) {
            console.error('Error submitting feedback:', error);
            feedbackMessage.textContent = '❌ Error submitting feedback. Please try again.';
            feedbackMessage.className = 'feedback-message error';
            feedbackMessage.style.display = 'block';
        }
    });
}

function showError(message) {
    const loadingState = document.getElementById('loadingState');
    const resultContainer = document.getElementById('resultContainer');
    const errorState = document.getElementById('errorState');
    const errorMessageEl = document.getElementById('errorMessage');

    loadingState.style.display = 'none';
    resultContainer.style.display = 'none';
    errorState.style.display = 'block';
    errorMessageEl.textContent = message;
}
