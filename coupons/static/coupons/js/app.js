
$(function() {
    $('.comment-form').each(function(index, form) {
        displayCommentForm(form)
        $(form).on('change', '[name=does_coupon_work]', function() {
            displayCommentForm(form)
        })
    })
})

function displayCommentForm(form) {
    var $form = $(form)
    if ($form.find('[name=does_coupon_work]:checked').length > 0) {
        $form.find('.comment-form-details').collapse('show')
    }
}