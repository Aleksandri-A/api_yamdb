from django.contrib import admin

from reviews.models import Review, Category, Comment, Genre, Title


admin.site.register(Review)
admin.site.register(Genre)
admin.site.register(Category)
admin.site.register(Title)
admin.site.register(Comment)
