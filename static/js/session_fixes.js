// Session and navigation fixes for Vercel deployment
document.addEventListener('DOMContentLoaded', function() {
    // Fix for profile links in deployed environment
    const profileLinks = document.querySelectorAll('.user-profile-link');
    
    profileLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // First verify the session is valid
            fetch('/verify-session')
                .then(response => response.json())
                .then(data => {
                    if (data.status === 'logged_in') {
                        // Session is valid, redirect to profile
                        window.location.href = '/profile';
                    } else {
                        // Session is invalid, redirect to login
                        alert('Your session has expired. Please login again.');
                        window.location.href = '/login_page';
                    }
                })
                .catch(error => {
                    console.error('Error checking session:', error);
                    window.location.href = '/profile'; // Try direct navigation as fallback
                });
        });
    });
});
