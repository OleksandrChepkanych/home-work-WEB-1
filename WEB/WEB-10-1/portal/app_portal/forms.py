from django.forms import ModelForm, CharField, TextInput, ModelChoiceField
from .models import Author, Quote, Tag


class AuthorForm(ModelForm):
    full_name = CharField(max_length=100, required=True, widget=TextInput)
    born_date = CharField(max_length=100, required=True, widget=TextInput)
    born_location = CharField(max_length=150, required=True, widget=TextInput)
    bio = CharField(max_length=1000, required=True, widget=TextInput)

    class Meta:
        model = Author
        fields = ['full_name', 'born_date', 'born_location', 'bio']


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class QuoteForm(ModelForm):
    author = ModelChoiceField(queryset=Author.objects.all())
    quote = CharField(max_length=2000, required=True, widget=TextInput)

    class Meta:
        model = Quote
        fields = ['author', 'quote']
        exclude = ['tags']