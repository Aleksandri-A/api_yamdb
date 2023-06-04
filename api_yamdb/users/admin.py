from django.contrib import admin
from .models import User
from reviews.models import Review, Genre, Category, Title, Comment
from users.models import Confirm


admin.site.register(User)
admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Comment)
admin.site.register(Confirm)
