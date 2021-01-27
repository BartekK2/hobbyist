from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Post, UserProfile, Category, Comment
from .utils import is_email_unique

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)
choice_list.sort()

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=False, max_length=100, validators=[is_email_unique])
    username = forms.CharField(required=True, min_length=4, max_length=16)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreatePostForm(forms.ModelForm):
    tytul = forms.CharField(required=True, max_length=50)
    class Meta:
        model = Post
        fields = ['tytul', 'opis', 'picture', 'category']
        widgets = {
            'opis': Textarea(attrs={'cols': 80, 'rows': 20, 'required': True}),
            'category': forms.Select(choices=choice_list),
        }


class UserProfileForm(forms.ModelForm):
    place = forms.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'fb', 'ig', 'tt', 'place']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': Textarea(attrs={'autofocus': True, 'required': True}),
        }

class SendMessageForm(forms.Form):
    title_email = forms.CharField(required=True, max_length=50,
                                  widget=forms.TextInput(attrs={'placeholder': 'Tytuł wiadomości'}))
    opis = forms.CharField(widget=forms.Textarea(
        attrs={'cols': 80, 'rows': 20, 'required': True, 'placeholder': 'Zawartość wiadomości'}), max_length=600)

