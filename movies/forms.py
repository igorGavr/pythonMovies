from django import forms

from .models import Reviews, RatingStar, Rating


class ReviewForm(forms.ModelForm):
    """ Форма відгуків """

    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    """"""
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(),
        widget=forms.RadioSelect(),
        empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)
