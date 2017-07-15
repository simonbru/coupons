from django import forms

from .models import Comment, Restaurant


class CommentForm(forms.ModelForm):
    restaurant = forms.ModelChoiceField(
        queryset=Restaurant.objects.by_distance(),
    )

    class Meta:
        model = Comment
        fields = [
            'does_coupon_work',
            'restaurant',
        ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Order choice of restaurant by distance
    #     self.fields['restaurant'].choices = [
    #         (None, '-----------')
    #     ] + [
    #         (resto.id, str(resto)) for resto in
    #         Restaurant.objects.by_distance()
    #     ]
