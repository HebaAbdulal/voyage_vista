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

    // Log the CSRF token and its length
    console.log('CSRF Token:', csrftoken);
    console.log('CSRF Token Length:', csrftoken.length);

    // Star rating handling
    $('.star').on('click', function() {
        var rating = $(this).data('value');

        $.ajax({
            type: 'POST',
            url: '/rate-post/' + postSlug + '/', // URL to the Django view
            headers: { 'X-CSRFToken': csrftoken }, // Use the CSRF token from the cookie
            data: JSON.stringify({ rating: rating }),
            contentType: 'application/json',
            success: function(response) {
                if (response.success) {
                    updateStars(rating);
                    $('#average-rating').text(response.average_rating.toFixed(1)); // Update average rating display
                } else {
                    alert('Error submitting rating: ' + response.error);
                }
            },
            error: function(xhr, status, error) {
                alert('Error submitting rating: ' + xhr.responseText);
            }
        });
    });

    // Hover effect for stars
    $('.star').hover(
        function() {
            var rating = $(this).data('value');
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
