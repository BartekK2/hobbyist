from django.db import models
from pathlib import Path
from django.contrib.auth.models import User
# To automatycznie zmienia rozdzielczość i format pliku na najodpowiedniejszy
from django_resized import ResizedImageField


BASE_DIR = Path(__file__).resolve().parent.parent


class Category(models.Model):
    name = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    tytul = models.CharField(max_length=60)
    opis = models.CharField(max_length=800, blank=True, null=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, default='')
    data = models.DateTimeField(auto_now_add=True)
    picture = ResizedImageField(size=[900, 700], quality=40,  upload_to='gallery/', blank=True)
    category = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.autor) + ' - Post Id: ' + str(self.id)



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fb = models.URLField(max_length=100, blank=True)
    ig = models.URLField(max_length=100, blank=True)
    tt = models.URLField(max_length=100, blank=True)
    birthday = models.DateField(null=True, blank=True)
    place = models.CharField(max_length=200, blank=True)
    profile_pic = ResizedImageField(size=[700, 700], quality=40, upload_to='gallery/', blank=True)

    def __str__(self):
        return self.user.username + " UP"

class Comment(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField(max_length=255, blank=False, default=None)

    def __str__(self):
        return self.autor.username + " - " + self.post.tytul
