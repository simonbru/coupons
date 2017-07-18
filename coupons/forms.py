from django import forms

from .models import Comment, Restaurant


class CommentForm(forms.ModelForm):
    does_coupon_work = forms.ChoiceField(
        choices=[
            (True, "Fonctionne"),
            (False, "Ne fonctionne pas"),
        ],
        widget=forms.RadioSelect,
    )
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
