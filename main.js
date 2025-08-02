// Court Case Lookup Portal - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Form validation and enhancement
    initializeFormValidation();
    
    // Loading states for forms
    initializeLoadingStates();
    
    // Auto-dismiss alerts
    initializeAlerts();
    
    console.log('Court Case Lookup Portal initialized');
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form validation and enhancement
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
                
                // Focus on first invalid field
                const firstInvalid = form.querySelector(':invalid');
                if (firstInvalid) {
                    firstInvalid.focus();
                    firstInvalid.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
            }
            
            form.classList.add('was-validated');
        });
    });
    
    // Case number formatting
    const caseNumberInput = document.getElementById('case_number');
    if (caseNumberInput) {
        caseNumberInput.addEventListener('input', function(e) {
            let value = e.target.value.toUpperCase();
            // Allow alphanumeric, forward slash, and hyphen
            value = value.replace(/[^A-Z0-9\/\-]/g, '');
            e.target.value = value;
        });
        
        caseNumberInput.addEventListener('blur', function(e) {
            validateCaseNumber(e.target);
        });
    }
    
    // Real-time validation feedback
    const requiredInputs = document.querySelectorAll('input[required], select[required]');
    requiredInputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateField(input);
        });
    });
}

// Validate case number format
function validateCaseNumber(input) {
    const value = input.value.trim();
    const feedbackElement = input.parentElement.querySelector('.invalid-feedback') || 
                           createFeedbackElement(input, 'invalid-feedback');
    
    if (value.length < 1) {
        input.classList.add('is-invalid');
        feedbackElement.textContent = 'Case number is required';
        return false;
    }
    
    if (value.length < 3) {
        input.classList.add('is-invalid');
        feedbackElement.textContent = 'Case number must be at least 3 characters';
        return false;
    }
    
    // Check for valid format (basic validation)
    if (!/^[A-Z0-9\/\-]+$/.test(value)) {
        input.classList.add('is-invalid');
        feedbackElement.textContent = 'Case number contains invalid characters';
        return false;
    }
    
    input.classList.remove('is-invalid');
    input.classList.add('is-valid');
    return true;
}

// Generic field validation
function validateField(input) {
    const value = input.value.trim();
    const isRequired = input.hasAttribute('required');
    
    if (isRequired && !value) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        return false;
    }
    
    if (value) {
        input.classList.remove('is-invalid');
        input.classList.add('is-valid');
    }
    
    return true;
}

// Create feedback element for validation
function createFeedbackElement(input, className) {
    const feedback = document.createElement('div');
    feedback.className = className;
    input.parentElement.appendChild(feedback);
    return feedback;
}

// Initialize loading states for form submissions
function initializeLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitButton = form.querySelector('button[type="submit"]');
            if (submitButton) {
                // Store original text
                const originalText = submitButton.innerHTML;
                
                // Add loading state
                submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Searching...';
                submitButton.disabled = true;
                submitButton.classList.add('loading');
                
                // Remove loading state after timeout (fallback)
                setTimeout(() => {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                    submitButton.classList.remove('loading');
                }, 30000); // 30 seconds timeout
            }
        });
    });
}

// Auto-dismiss alerts after a delay
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    
    alerts.forEach(alert => {
        // Auto-dismiss after 10 seconds for non-error alerts
        if (!alert.classList.contains('alert-danger')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                try {
                    bsAlert.close();
                } catch (e) {
                    // Alert might already be closed
                }
            }, 10000);
        }
    });
}

// Utility function to show custom alerts
function showAlert(message, type = 'info', permanent = false) {
    const alertContainer = document.querySelector('.container');
    if (!alertContainer) return;
    
    const alertElement = document.createElement('div');
    alertElement.className = `alert alert-${type} alert-dismissible fade show ${permanent ? 'alert-permanent' : ''}`;
    alertElement.innerHTML = `
        <i class="fas fa-${getAlertIcon(type)} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at the top of the container
    alertContainer.insertBefore(alertElement, alertContainer.firstChild);
    
    // Auto-dismiss if not permanent
    if (!permanent && type !== 'danger') {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alertElement);
            try {
                bsAlert.close();
            } catch (e) {
                // Alert might already be closed
            }
        }, 8000);
    }
}

// Get appropriate icon for alert type
function getAlertIcon(type) {
    const icons = {
        'success': 'check-circle',
        'info': 'info-circle',
        'warning': 'exclamation-triangle',
        'danger': 'exclamation-circle'
    };
    return icons[type] || 'info-circle';
}

// Smooth scroll to element
function scrollToElement(element, offset = 0) {
    if (typeof element === 'string') {
        element = document.querySelector(element);
    }
    
    if (element) {
        const elementPosition = element.offsetTop - offset;
        window.scrollTo({
            top: elementPosition,
            behavior: 'smooth'
        });
    }
}

// Format date for display
function formatDate(dateString, format = 'long') {
    if (!dateString) return 'Not available';
    
    const date = new Date(dateString);
    const options = format === 'long' 
        ? { year: 'numeric', month: 'long', day: 'numeric' }
        : { year: 'numeric', month: 'short', day: 'numeric' };
    
    return date.toLocaleDateString('en-IN', options);
}

// Copy text to clipboard
function copyToClipboard(text, successMessage = 'Copied to clipboard') {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert(successMessage, 'success');
        }).catch(err => {
            console.error('Failed to copy: ', err);
            showAlert('Failed to copy to clipboard', 'warning');
        });
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.select();
        try {
            document.execCommand('copy');
            showAlert(successMessage, 'success');
        } catch (err) {
            console.error('Failed to copy: ', err);
            showAlert('Failed to copy to clipboard', 'warning');
        }
        document.body.removeChild(textArea);
    }
}

// Export functions for use in other scripts
window.CourtPortal = {
    showAlert,
    scrollToElement,
    formatDate,
    copyToClipboard,
    validateCaseNumber
};
