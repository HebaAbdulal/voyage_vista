function toggleEditForm(commentId) {
    var editForm = document.getElementById('edit-form-' + commentId);
    var commentActions = document.getElementById('comment-actions-' + commentId);

    if (editForm.style.display === 'none') {
        editForm.style.display = 'block';
        commentActions.style.display = 'none';
    } else {
        editForm.style.display = 'none';
        commentActions.style.display = 'block';
    }
}

function submitEdit(commentId, postSlug) {
    var editForm = document.getElementById('edit-form-' + commentId);
    var formData = new FormData(editForm);
    formData.append('comment_id', commentId);

    fetch(`/comment/${postSlug}/${commentId}/edit/`, {
        method: "POST",
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': getCookie('csrftoken')
        }
    }).then(response => response.json())
      .then(data => {
          if (data.success) {
              alert(data.message);
              location.reload();
          } else {
              alert(data.error);
          }
      }).catch(error => console.log(error));
}

function confirmDeletion() {
    return confirm('Are you sure you want to delete this comment?');
}

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