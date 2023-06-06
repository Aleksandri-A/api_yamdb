from django.contrib import admin

from reviews.models import Category, Comment, Genre, Review, Title
from .models import User

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Comment)
