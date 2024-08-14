$(document).ready(function() {
    // Star rating handling
    $('.star').on('click', function() {
        var rating = $(this).data('value');
        var postSlug = "{{ post.slug }}";  // Add post slug dynamically

        $.ajax({
            type: 'POST',
            url: '/rate-post/' + postSlug + '/',
            headers: { 'X-CSRFToken': '{{ csrf_token }}' },
            data: JSON.stringify({ rating: rating }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    updateStars(rating);
                } else {
                    alert('Error submitting rating');
                }
            }
        });
    });

    // Hover effect for stars
    $('.star').hover(
        function() {
            var rating = $(this).data('value');
            updateStars(rating);
        }, function() {
            var rating = '{{ user_rating.rating }}';  // Add user's rating dynamically if available
            updateStars(rating);
        }
    );

    // Function to update stars
    function updateStars(rating) {
        $('.star').each(function() {
            if ($(this).data('value') <= rating) {
                $(this).addClass('selected');
            } else {
                $(this).removeClass('selected');
            }
        });
    }

    // Initialize stars based on user rating
    updateStars('{{ user_rating.rating }}');
});

document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('rate-form').addEventListener('submit', function(event) {
        event.preventDefault();

        let ratingValue = document.querySelector('input[name="rating"]:checked').value;
        let postSlug = this.dataset.postSlug;

        fetch(`/rate/${postSlug}/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({ rating: ratingValue })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Display success message to the user
                let messageDiv = document.getElementById('message');
                messageDiv.textContent = data.message;
                messageDiv.style.display = 'block';
                messageDiv.classList.add('success-message'); // Optional: add a CSS class for styling
            } else {
                // Handle errors if necessary
                console.error('Error:', data.error);
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Function to get CSRF token from cookies
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            let cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                let cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});