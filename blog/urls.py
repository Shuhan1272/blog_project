# blog/urls.py
from django.urls import path
from . import views

# Note : Order of URL patterns
#If you already defined favorites/, check the order. Django matches top to bottom. If your path("blogs/<slug:slug>/", ...) comes before path("blogs/favorites/", ...), then "favorites" will never reach the correct view.

urlpatterns = [
    # Example homepage for blog
    path('', views.home, name='home'),
    path('create/', views.create_blog, name='create_blog'),
    path('favorites/', views.favorites_list, name='favorites_list'),
    path('<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('<slug:slug>/edit/', views.edit_blog, name='edit_blog'),
    path('<slug:slug>/delete/', views.delete_blog, name='delete_blog'), 
    path('<slug:slug>/review/', views.review_blog, name='review_blog'), 
    path('<slug:slug>/reviews/', views.blog_reviews, name='blog_reviews'), 
    path('<slug:slug>/delete/review/', views.delete_review, name='delete_review'),
    path('toggle_favorite/<slug:slug>/', views.toggle_favorite, name='toggle_favorite'),

]
