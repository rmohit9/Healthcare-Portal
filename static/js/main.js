// Healthcare Portal JavaScript with Blog Functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    initializeApp();
});

function initializeApp() {
    // Add fade-in animation to cards
    addFadeInAnimation();

    // Initialize form validation
    initializeFormValidation();

    // Initialize profile picture preview
    initializeProfilePicturePreview();

    // Initialize blog features
    initializeBlogFeatures();

    // Initialize tooltips
    initializeTooltips();
}

// Add fade-in animation to elements
function addFadeInAnimation() {
    const cards = document.querySelectorAll('.card');
    cards.forEach((card, index) => {
        setTimeout(() => {
            card.classList.add('fade-in-up');
        }, index * 100);
    });
}

// Form validation
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
            }
        });

        // Real-time validation
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
    });
}

// Validate individual field
function validateField(field) {
    const value = field.value.trim();
    const fieldName = field.name;
    let isValid = true;
    let errorMessage = '';

    // Remove existing error messages
    removeFieldError(field);

    // Required field validation
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        errorMessage = 'This field is required.';
    }

    // Email validation
    else if (field.type === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            errorMessage = 'Please enter a valid email address.';
        }
    }

    // Password validation
    else if (fieldName === 'password1' && value) {
        if (value.length < 8) {
            isValid = false;
            errorMessage = 'Password must be at least 8 characters long.';
        }
    }

    // Confirm password validation
    else if (fieldName === 'password2' && value) {
        const password1 = document.querySelector('input[name="password1"]');
        if (password1 && value !== password1.value) {
            isValid = false;
            errorMessage = 'Passwords do not match.';
        }
    }

    // Pincode validation
    else if (fieldName === 'pincode' && value) {
        const pincodeRegex = /^[0-9]{5,6}$/;
        if (!pincodeRegex.test(value)) {
            isValid = false;
            errorMessage = 'Pincode must be 5 or 6 digits.';
        }
    }

    // Blog title validation
    else if (fieldName === 'title' && value) {
        if (value.length < 5) {
            isValid = false;
            errorMessage = 'Title must be at least 5 characters long.';
        }
    }

    // Blog summary validation
    else if (fieldName === 'summary' && value) {
        if (value.length < 20) {
            isValid = false;
            errorMessage = 'Summary must be at least 20 characters long.';
        } else if (value.length > 500) {
            isValid = false;
            errorMessage = 'Summary must not exceed 500 characters.';
        }
    }

    // Blog content validation
    else if (fieldName === 'content' && value) {
        if (value.length < 100) {
            isValid = false;
            errorMessage = 'Content must be at least 100 characters long.';
        }
    }

    if (!isValid) {
        showFieldError(field, errorMessage);
    }

    return isValid;
}

// Validate entire form
function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');

    inputs.forEach(input => {
        if (!validateField(input)) {
            isValid = false;
        }
    });

    // Additional form-specific validation
    if (form.id === 'signup-form') {
        const password1 = form.querySelector('input[name="password1"]');
        const password2 = form.querySelector('input[name="password2"]');

        if (password1 && password2 && password1.value !== password2.value) {
            showFieldError(password2, 'Passwords do not match.');
            isValid = false;
        }
    }

    return isValid;
}

// Show field error
function showFieldError(field, message) {
    removeFieldError(field);

    field.classList.add('is-invalid');

    const errorDiv = document.createElement('div');
    errorDiv.className = 'invalid-feedback';
    errorDiv.textContent = message;

    field.parentNode.appendChild(errorDiv);
}

// Remove field error
function removeFieldError(field) {
    field.classList.remove('is-invalid');
    const existingError = field.parentNode.querySelector('.invalid-feedback');
    if (existingError) {
        existingError.remove();
    }
}

// Profile picture preview
function initializeProfilePicturePreview() {
    const profileInput = document.querySelector('input[name="profile_picture"]');

    if (profileInput) {
        profileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (file) {
                const reader = new FileReader();

                reader.onload = function(e) {
                    // Create or update preview
                    let preview = document.getElementById('profile-preview');

                    if (!preview) {
                        preview = document.createElement('img');
                        preview.id = 'profile-preview';
                        preview.className = 'img-thumbnail mt-2';
                        preview.style.maxWidth = '200px';
                        profileInput.parentNode.appendChild(preview);
                    }

                    preview.src = e.target.result;
                };

                reader.readAsDataURL(file);
            }
        });
    }
}

// Blog-specific features
function initializeBlogFeatures() {
    // Initialize blog image preview
    initializeBlogImagePreview();

    // Initialize character counters
    initializeCharacterCounters();

    // Initialize search functionality
    initializeSearch();

    // Initialize category filtering
    initializeCategoryFilter();
}

// Blog image preview
function initializeBlogImagePreview() {
    const imageInput = document.querySelector('input[name="image"]');

    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            const file = e.target.files[0];

            if (file) {
                // Validate file type
                const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif'];
                if (!allowedTypes.includes(file.type)) {
                    showNotification('Please select a valid image file (JPEG, PNG, or GIF).', 'warning');
                    this.value = '';
                    return;
                }

                // Validate file size (max 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    showNotification('Image file size must be less than 5MB.', 'warning');
                    this.value = '';
                    return;
                }

                const reader = new FileReader();

                reader.onload = function(e) {
                    // Remove existing preview
                    const existingPreview = document.querySelector('#blog-image-preview');
                    if (existingPreview) {
                        existingPreview.remove();
                    }

                    // Create new preview
                    const preview = document.createElement('div');
                    preview.id = 'blog-image-preview';
                    preview.className = 'mt-2';
                    preview.innerHTML = `
                        <small class="text-muted">Preview:</small><br>
                        <img src="${e.target.result}" alt="Blog image preview" class="img-thumbnail" style="max-width: 300px; max-height: 200px;">
                    `;
                    imageInput.parentNode.appendChild(preview);
                };

                reader.readAsDataURL(file);
            }
        });
    }
}

// Character counters for blog forms
function initializeCharacterCounters() {
    // Summary counter
    const summaryField = document.querySelector('textarea[name="summary"]');
    if (summaryField) {
        const counter = document.createElement('small');
        counter.className = 'text-muted float-end';
        counter.id = 'summary-counter';

        const helpText = summaryField.parentNode.querySelector('.form-text');
        if (helpText) {
            helpText.appendChild(counter);
        }

        function updateSummaryCounter() {
            const count = summaryField.value.length;
            counter.textContent = `${count}/500 characters`;

            if (count > 500) {
                counter.classList.add('text-danger');
                summaryField.classList.add('is-invalid');
            } else {
                counter.classList.remove('text-danger');
                summaryField.classList.remove('is-invalid');
            }
        }

        summaryField.addEventListener('input', updateSummaryCounter);
        updateSummaryCounter();
    }

    // Content counter
    const contentField = document.querySelector('textarea[name="content"]');
    if (contentField) {
        const counter = document.createElement('small');
        counter.className = 'text-muted float-end';
        counter.id = 'content-counter';

        const helpText = contentField.parentNode.querySelector('.form-text');
        if (helpText) {
            helpText.appendChild(counter);
        }

        function updateContentCounter() {
            const count = contentField.value.length;
            const words = contentField.value.trim().split(/\s+/).length;
            counter.textContent = `${count} characters, ${words} words`;
        }

        contentField.addEventListener('input', updateContentCounter);
        updateContentCounter();
    }
}

// Search functionality
function initializeSearch() {
    const searchForm = document.querySelector('form[method="get"]');
    const searchInput = document.querySelector('input[name="search"]');

    if (searchForm && searchInput) {
        // Add search suggestions (placeholder for future enhancement)
        searchInput.addEventListener('focus', function() {
            this.placeholder = 'Search by title, summary, or content...';
        });

        searchInput.addEventListener('blur', function() {
            this.placeholder = 'Search blog posts...';
        });
    }
}

// Category filtering
function initializeCategoryFilter() {
    const categorySelect = document.querySelector('select[name="category"]');

    if (categorySelect) {
        categorySelect.addEventListener('change', function() {
            if (this.value) {
                // Auto-submit form when category is selected
                this.form.submit();
            }
        });
    }
}

// Initialize Bootstrap tooltips
function initializeTooltips() {
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

// Utility functions
function showNotification(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        <i class="fas fa-info-circle me-2"></i>${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    const container = document.querySelector('.container');
    if (container) {
        container.insertBefore(alertDiv, container.firstChild);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (alertDiv.parentNode) {
                alertDiv.remove();
            }
        }, 5000);
    }
}

// Loading state for buttons
function setButtonLoading(button, loading = true) {
    if (loading) {
        button.disabled = true;
        button.classList.add('loading');
        button.dataset.originalText = button.textContent;
    } else {
        button.disabled = false;
        button.classList.remove('loading');
        if (button.dataset.originalText) {
            button.textContent = button.dataset.originalText;
        }
    }
}

// Smooth scrolling for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth'
            });
        }
    });
});

// Reading time calculator for blog posts
function calculateReadingTime(content) {
    const wordsPerMinute = 200;
    const words = content.trim().split(/\s+/).length;
    return Math.ceil(words / wordsPerMinute);
}

// Text truncation helper
function truncateText(text, wordLimit) {
    const words = text.split(' ');
    if (words.length > wordLimit) {
        return words.slice(0, wordLimit).join(' ') + '...';
    }
    return text;
}

// Debounce function
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}