from django import forms

from .models import Comment, Restaurant


class RadioButtonSelect(forms.RadioSelect):
    option_template_name = 'widgets/radio_button_option.html'


class CommentChoice(str):
    """Hack to pass more attributes to each radio option

    Since we can only pass a value and a label for each choice,
    we set additional attributes on the label string instead.
    """
    def __new__(cls, value, css_classes='btn-primary', bs_icon=None):
        string = super().__new__(cls, value)
        string.css_classes = css_classes
        string.bs_icon = bs_icon
        return string


class CommentForm(forms.ModelForm):
    does_coupon_work = forms.ChoiceField(
        choices=[
            (True, CommentChoice(
                "Fonctionne", 'btn-success', 'thumbs-up'
            )),
            (False, CommentChoice(
                "Ne fonctionne pas", 'btn-danger', 'thumbs-down'
            )),
        ],
        widget=RadioButtonSelect,
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
