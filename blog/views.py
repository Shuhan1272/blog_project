from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Blog, Category, Review, Favorite
from .forms import ReviewForm
from django.db.models import Avg, Q
from django.contrib.auth.decorators import login_required
from .utils import send_confirmation_email
from django.contrib import messages  

from blog.models import Blog


def home(request):
    blogs = Blog.objects.all().select_related('author').prefetch_related('categories', 'reviews').order_by('-created_at')   
    categories = Category.objects.all()
    authors = set(blog.author for blog in blogs)

    # --- Filters ---
    q = request.GET.get("q")
    category = request.GET.get("category")
    author = request.GET.get("author")
    date = request.GET.get("date")
    sort = request.GET.get("sort")

    if q:
        blogs = blogs.filter(Q(title__icontains=q) | Q(body__icontains=q))

    if category:
        blogs = blogs.filter(categories__slug=category)

    if author:
        blogs = blogs.filter(author__id=author)

    if date:
        blogs = blogs.filter(created_at__date=date)

    if sort == "latest":
        blogs = blogs.order_by("-created_at")
    elif sort == "rating":
        blogs = blogs.annotate(avg_rating=Avg("reviews__rating")).order_by("-avg_rating")

    for blog in blogs:
        blog.avg_rating = blog.reviews.aggregate(Avg("rating"))["rating__avg"]
        blog.review_count = blog.reviews.count()
        if request.user.is_authenticated:
            blog.user_review = blog.reviews.filter(user=request.user).first()
            blog.is_favorited = Favorite.objects.filter(blog=blog, user=request.user).exists()
        else:
            blog.is_favorited = False
    
    return render(request, 'blog/home.html', {'blogs': blogs, 'categories': categories, 'authors': authors})


def blog_detail(request, slug):
    blog = Blog.objects.get(slug=slug)
    blog.avg_rating = blog.reviews.aggregate(Avg("rating"))["rating__avg"]
    blog.review_count = blog.reviews.count()
    if request.user.is_authenticated:
        blog.user_review = blog.reviews.filter(user=request.user).first()
        blog.is_favorited = Favorite.objects.filter(blog=blog, user=request.user).exists()
    else:
        blog.is_favorited = False
    return render(request, 'blog/blog_detail.html', {'blog': blog})


@login_required
def create_blog(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        title = request.POST.get('title')
        body = request.POST.get('body')
        category_ids = request.POST.getlist('categories')
        blog = Blog.objects.create(title=title, body=body, author=request.user)
        blog.categories.set(category_ids)
        messages.success(request, "Your blog has been created successfully ✅")  # ✅
        return redirect('blog_detail', slug=blog.slug)
    return render(request, 'blog/create_blog.html', {'categories': categories})


@login_required
def edit_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    categories = Category.objects.all()
    if request.method == 'POST':
        blog.title = request.POST.get('title')
        blog.body = request.POST.get('body')
        blog.categories.set(request.POST.getlist('categories'))
        blog.save()
        messages.success(request, "Blog updated successfully ✏️")  # ✅
        return redirect('blog_detail', slug=blog.slug)
    return render(request, 'blog/edit_blog.html', {'form': blog, 'categories': categories})

@login_required
def delete_blog(request, slug):
    blog = Blog.objects.get(slug=slug)
    if request.method == 'POST':
        blog.delete()
        messages.success(request, "Blog deleted successfully.")
        return redirect('home')
    messages.error(request, "Invalid request method.")
    return redirect('home')


# review_blog
@login_required
def review_blog(request, slug):
    url = request.META.get('HTTP_REFERER')
    blog = get_object_or_404(Blog, slug=slug)

    review, created = Review.objects.get_or_create(
        blog=blog,
        user=request.user,
        defaults={"rating": 0, "review": ""}
    )

    if request.method == "POST":
        review.rating = request.POST.get("rating")
        review.review = request.POST.get("review")
        review.save()
        if created:
            messages.success(request, "Your review has been added ⭐")  # ✅
        else:
            messages.success(request, "Your review has been updated ✏️")  # ✅
        return redirect(url)

    messages.error(request, "Invalid request method.")
    return redirect(url or 'home')


def blog_reviews(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    sort = request.GET.get("sort", "newest")
    reviews = Review.objects.filter(blog=blog)

    if sort == "oldest":
        reviews = reviews.order_by("created_at")
    elif sort == "highest":
        reviews = reviews.order_by("-rating")
    elif sort == "lowest":
        reviews = reviews.order_by("rating")
    else:
        reviews = reviews.order_by("-created_at")

    avg_rating = reviews.aggregate(Avg("rating"))["rating__avg"]

    return render(request, "blog/blog_reviews.html", {
        "blog": blog,
        "reviews": reviews,
        "avg_rating": avg_rating,
    })


# delete_review
@login_required
def delete_review(request, slug):
    url = request.META.get('HTTP_REFERER')
    blog = get_object_or_404(Blog, slug=slug)
    review = get_object_or_404(Review, blog=blog, user=request.user)

    if request.method == "POST":
        review.delete()
        messages.success(request, "Your review has been deleted.")
        return redirect(url)

    messages.error(request, "Invalid request method.")
    return redirect(url or 'home')


@login_required
def toggle_favorite(request, slug):
    blog = get_object_or_404(Blog, slug=slug)

    favorite, created = Favorite.objects.get_or_create(
        blog=blog,
        user=request.user
    )

    if created:
        send_confirmation_email(request, request.user, blog)
        messages.success(request, f"‘{blog.title}’ added to favorites ❤️")  # ✅
    else:
        favorite.delete()
        messages.warning(request, f"‘{blog.title}’ removed from favorites 💔")  # ✅

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user)
    return render(request, 'blog/favorites_list.html', {'favorites': favorites})
