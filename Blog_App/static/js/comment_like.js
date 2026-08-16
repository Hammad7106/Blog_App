  $(document).ready(function() {
    $('.like-comments').on('click', function() {
        var commentId = $(this).data('comment-id');
        var likeButton = $(this);

        $.ajax({
            type: 'POST',
            url: `/comment/${commentId}/like/`,
            data: {
                csrfmiddlewaretoken: '{{ csrf_token }}'
            },
            success: function(response) {
                if (response.status === 'success') {
                    if (response.action === 'liked') {
                        // Update UI to reflect liked status
                        likeButton.text('Liked');
                    } else if (response.action === 'unliked') {
                        // Update UI to reflect unliked status
                        likeButton.text('Like');
                    }
                } else {
                    alert(response.message);
                }
            },
            error: function(xhr) {
                alert('An error occurred. Please try again.');
            }
        });
    });
});
