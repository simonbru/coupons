from typing import Optional, Iterable

from django import forms

from .models import Comment, Restaurant


class TextInputWithAutocomplete(forms.TextInput):
    template_name = 'widgets/text_autocomplete.html'
    datalist_id: Optional[str]
    choices: Iterable[str]

    def __init__(self, *args, datalist_id=None, choices=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.datalist_id = datalist_id
        if choices is None:
            choices = []
        self.choices = choices

    def get_datalist_id(self, attrs):
        """
        Generate datalist id from input id
        if `datalist_id` was not specified
        """
        if self.datalist_id is not None:
            datalist_id = self.datalist_id
        else:
            datalist_id = attrs.get('id', '') + '--datalist'
        return datalist_id

    def build_attrs(self, *args, **kwargs):
        attrs = super().build_attrs(*args, **kwargs)
        attrs.setdefault('list', self.get_datalist_id(attrs))
        return attrs

    def get_context(self, name, value, attrs):
        return {
            **super().get_context(name, value, attrs),
            'choices': self.choices
        }


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

    def sort_restaurants_by_distance(self, lat, lon):
        field = self.fields['restaurant']
        field.queryset = Restaurant.objects.by_distance(lat, lon)
        # Use closest restaurant as initial value if not already set
        if self.get_initial_for_field(field, 'restaurant') is None:
            self.initial['restaurant'] = field.queryset.first().pk


    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     # Order choice of restaurant by distance
    #     self.fields['restaurant'].choices = [
    #         (None, '-----------')
    #     ] + [
    #         (resto.id, str(resto)) for resto in
    #         Restaurant.objects.by_distance()
    #     ]
