from .models import Publisher, Review,Contributor
from django import forms

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = "__all__"

class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=(("title", "Title"), ("contributor", "Contributor")))

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "book"]

    rating = forms.IntegerField(min_value=0, max_value=5)

class ContributorForm(forms.ModelForm):
    class Meta:
        model = Contributor
        fields = "__all__"
