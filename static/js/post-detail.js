


// Function to toggle the visibility of the edit form
var toggleEditForm = function(commentId) {
    var editForm = document.getElementById('edit-form-' + commentId);
    var commentActions = document.getElementById('comment-actions-' + commentId);

    if (editForm.style.display === 'none') {
        editForm.style.display = 'block';
        commentActions.style.display = 'none';
    } else {
        editForm.style.display = 'none';
        commentActions.style.display = 'block';
    }
};

// Function to submit the edited comment via AJAX
var submitEdit = function(commentId, postSlug) {
    var editForm = document.getElementById('edit-form-' + commentId);
    var formData = new FormData(editForm);
    formData.append('comment_id', commentId);

    fetch('/comment/' + postSlug + '/' + commentId + '/edit/', {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error);
        }
    })
    .catch(function(error) {
        console.error(error);
    });
};

// Function to confirm deletion of a comment
var confirmDeletion = function() {
    return confirm('Are you sure you want to delete this comment?');
};

// Function to get CSRF token from cookies
var getCookie = function(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.indexOf(name + '=') === 0) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
};
