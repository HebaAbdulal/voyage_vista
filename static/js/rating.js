$(document).ready(function() {
    // Function to get the CSRF token from the cookie
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Ensure postSlug and userRating are logged
    console.log('Post Slug:', postSlug);
    console.log('User Rating:', userRating);

    // Star rating handling
    $('.star').on('click', function() {
        const rating = $(this).data('value');

        $.ajax({
            type: 'POST',
            url: `/rate-post/${postSlug}/`, // Correctly use the postSlug variable here
            headers: { 'X-CSRFToken': csrftoken }, // Use the CSRF token from the cookie
            data: JSON.stringify({ rating: rating }),
            contentType: 'application/json',
            success: function(response) {
                console.log('AJAX Success:', response); // Debugging
                if (response.success) {
                    updateStars(rating);
                    $('#average-rating').text(response.average_rating.toFixed(1)); // Update average rating display

                    // Display the success message
                    $('#message-container')
                        .text(response.message)
                        .removeClass() // Remove any existing classes
                        .addClass('alert alert-success') // Add Bootstrap success classes
                        .fadeIn() // Fade in the message
                        .delay(3000) // Wait for 3 seconds
                        .fadeOut(); // Fade out the message
                } else {
                    alert('Error submitting rating: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                console.error('AJAX Error:', xhr.responseText); // Debugging
                alert('Error submitting rating: ' + xhr.responseText);
            }
        });
    });

    // Hover effect for stars
    $('.star').hover(
        function() {
            const rating = $(this).data('value');
            updateStars(rating);
        }, function() {
            updateStars(userRating); // Restore user's rating on hover out
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
    updateStars(userRating);
});
