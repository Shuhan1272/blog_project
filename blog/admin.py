from django.contrib import admin
from .models import Blog,Category, Review,Favorite

# Register your models here.
admin.site.register(Blog)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Favorite)