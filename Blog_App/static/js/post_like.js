$(document).ready(function() {
    $('.like-button').each(function() {
        var likeButton = $(this);
        var likeCountElement = likeButton.siblings('.like-count');
        var postID = likeButton.data('post-id');

        $.ajax({
            url: `/check_like/${postID}/`,  // URL to check if user liked the post
            method: 'GET',
            success: function(response) {
                if (response.user_liked) {
                    likeButton.text('Dislike');
                }
            },
            error: function(error) {
                console.log(error);
            }
        });

        likeButton.on('click', function(event) {
            event.preventDefault();

            var csrfToken = $('input[name=csrfmiddlewaretoken]').val(); // Get the CSRF token

            $.ajax({
                url: `/like/${postID}/`, // URL for 'LikeView' to like/unlike the post
                method: 'POST',
                data: { csrfmiddlewaretoken: csrfToken }, // Include the CSRF token in the data
                success: function(response) {
                    likeCountElement.text(response.like_count);
                    if (likeButton.text() === 'Like') {
                        likeButton.text('Dislike');
                    } else {
                        likeButton.text('Like');
                    }
                },
                error: function(error) {
                    console.log(error);
                }
            });
        });
    });
});
