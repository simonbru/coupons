
$(function() {
    $('.comment-form').each(function(index, form) {
        displayCommentForm(form)
        $(form).on('change', '[name=does_coupon_work]', function() {
            displayCommentForm(form)
        })
    })
})

function displayCommentForm(form) {
    if (form['does_coupon_work'].value) {
        $(form).find('.comment-form-details').collapse('show')
    }
}