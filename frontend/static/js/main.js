/**
 * Main Dashboard Script
 * Handles form submission and API communication
 */

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('recommendationForm');
    const phSlider = document.getElementById('phSlider');
    const phValue = document.getElementById('phValue');
    const submitBtn = document.getElementById('submitBtn');
    const loadingIndicator = document.getElementById('loadingIndicator');
    const errorMessage = document.getElementById('errorMessage');

    // Update pH value display
    phSlider.addEventListener('input', function() {
        phValue.textContent = this.value;
    });

    // Form submission
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        try {
            // Validate form
            if (!form.checkValidity()) {
                showError('Please fill in all required fields');
                return;
            }

            // Get form data
            const formData = new FormData(form);
            const data = {
                nitrogen: parseFloat(formData.get('nitrogen')),
                phosphorus: parseFloat(formData.get('phosphorus')),
                potassium: parseFloat(formData.get('potassium')),
                temperature: parseFloat(formData.get('temperature')),
                temperature_unit: formData.get('temperature_unit'),
                humidity: parseFloat(formData.get('humidity')),
                rainfall: parseFloat(formData.get('rainfall')),
                ph: parseFloat(formData.get('ph')),
                season: formData.get('season'),
                location: formData.get('location')
            };

            console.log('Sending data:', data);

            // Show loading state
            showLoading(true);
            errorMessage.style.display = 'none';

            // Send request to backend
            const response = await fetch('/api/recommend', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(data)
            });

            showLoading(false);

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || 'Failed to get recommendation');
            }

            const result = await response.json();
            console.log('Recommendation received:', result);

            // Store recommendation in session storage for output page
            sessionStorage.setItem('recommendation', JSON.stringify({
                input: data,
                result: result,
                timestamp: new Date().toISOString()
            }));

            // Redirect to output page
            window.location.href = '/output';

        } catch (error) {
            console.error('Error:', error);
            showLoading(false);
            showError(error.message || 'An unexpected error occurred. Please try again.');
        }
    });

    function showLoading(show) {
        if (show) {
            loadingIndicator.style.display = 'block';
            submitBtn.disabled = true;
            submitBtn.querySelector('.btn-text').style.display = 'none';
            submitBtn.querySelector('.btn-loader').style.display = 'flex';
        } else {
            loadingIndicator.style.display = 'none';
            submitBtn.disabled = false;
            submitBtn.querySelector('.btn-text').style.display = 'inline';
            submitBtn.querySelector('.btn-loader').style.display = 'none';
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.style.display = 'block';
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    // Form reset handler
    form.addEventListener('reset', function() {
        phValue.textContent = '7.0';
        phSlider.value = '7';
        errorMessage.style.display = 'none';
    });
});
