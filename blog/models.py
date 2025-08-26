from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.utils.text import slugify
from django.db.models import Avg
from accounts.models import CustomUser


class TimeStampedModel(models.Model):

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True #means for this class inside database table will be not created.. this class will be inherited by other classes. 


class Category(TimeStampedModel): #here timestampedmodel inherited models.Model that is why we don't need inherit models.Model again. Note : all the field of timestampedmodel will come in this class. 
    category_name = models.CharField(max_length=100)

    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs): 
        self.slug = slugify(self.category_name)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.category_name


class Blog(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(blank=True, unique=True)
    body = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="blogs")
    categories = models.ManyToManyField(Category, related_name="blogs", blank=True)
    
    def save(self, *args, **kwargs): 
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.title 
    


class Review(TimeStampedModel):
    blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="reviews"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    rating = models.FloatField()
    review = models.TextField(max_length=500, blank=True)

    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.user.first_name} for {self.blog.title}"

class Favorite(TimeStampedModel):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="favorites")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="favorites")

    def __str__(self):
        return f"Favorite by {self.user.first_name} for {self.blog.title}"
