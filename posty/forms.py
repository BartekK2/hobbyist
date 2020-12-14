from django.core.exceptions import ValidationError
from django.forms import ModelForm, Textarea
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Post, UserProfile, Category, Comment

choices = Category.objects.all().values_list('name', 'name')
choice_list = []
for item in choices:
    choice_list.append(item)
choice_list.sort()

# Błąd podczas tworzenia migracji ale działa poprawnie dopuki nie rozwiazesz problemu uzywaj
# python manage.py makemigrations posty python manege.py migrate :)
User._meta.get_field('email')._unique = True

class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=False, max_length=100)
    username = forms.CharField(required=True, min_length=4, max_length=16)
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CreatePostForm(forms.ModelForm):
    tytul = forms.CharField(required=True)
    class Meta:
        model = Post
        fields = ['tytul', 'opis', 'picture', 'category']
        widgets = {
            'opis': Textarea(attrs={'cols': 80, 'rows': 20,'required': True}),
            'category': forms.Select(choices=choice_list),
        }


class UserProfileForm(forms.ModelForm):
    place = forms.CharField(required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_pic', 'fb', 'ig', 'tt', 'birthday', 'place']


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']