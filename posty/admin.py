from django.contrib import admin

# Register your models here.
from .models import Post, UserProfile, Category, Comment
admin.site.register(Post)
admin.site.register(UserProfile)
admin.site.register(Category)
admin.site.register(Comment)