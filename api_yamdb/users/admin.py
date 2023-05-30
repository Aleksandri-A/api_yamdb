from django.contrib import admin
from .models import User
from reviews.models import Reviews, Genres, Categories, Titles


admin.site.register(User)
admin.site.register(Reviews)
admin.site.register(Genres)
admin.site.register(Categories)
admin.site.register(Titles)
