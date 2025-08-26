from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import redirect, render
from django.utils.http import urlsafe_base64_decode

from accounts.forms import CustomUserForm,CustomAuthenticationForm,UserProfileForm
from accounts.models import CustomUser
from accounts.utils import send_verification_email,send_password_reset_email

from django.contrib.auth.forms import SetPasswordForm,PasswordChangeForm

from blog.models import Blog
from django.db.models import Avg

# Create your views here.

def signup(request):
    if request.method == "POST":
        form = CustomUserForm(request.POST) #getting form data. 
        if form.is_valid(): #checking form validation# All the validation will be cheaked as we inherited UserCreationForm build in form in CustomUserForm

            user = form.save()

            send_verification_email(request, user)
            messages.info(request, "We have sent you an verfication email")

            messages.success(request, 'Registration successfull.')

            return redirect('signup')
    else:
        form = CustomUserForm()        
    context = {
        "form" : form 
    }
    #Note : passing form is mandatory for print form errors 
    return render(request,'accounts/signup.html',context)

def verify_email(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token): #checking this token was created for this user or not. 
        user.is_verified = True
        user.save()
        messages.success(request, "Your email has been verified successfully.")
        return redirect("login")
    else:
        messages.info(request, "The verification link is invalid or has expired.")
        return redirect("signup")

def user_login(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            if not user.is_verified:
                messages.info(request,"Your email is not verified yet.")
            else:
                
                login(request,user)
                messages.success(request,"You are logged in successfully")
                return redirect('home')
    else:
        form = CustomAuthenticationForm(request)

    context = {
        "form" : form 
    }
        
    return render(request, "accounts/login.html",context)


@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"You have logout successfully.")
    return redirect('login')

def reset_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User does not exist.")
            return redirect("password-reset")

        send_password_reset_email(request, user)
        messages.info(
            request, "We have sent you an email with password reset instructions"
        )
        return redirect("login")

    return render(request, "accounts/forgot.html")

def reset_password_confirm(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_verified = True
        user.save()
        user.backend = 'accounts.authentication.EmailBackend'
        login(request, user)
        return redirect("new-password")
    else:
        messages.error(request, "The verification link is invalid or has expired.")
        return redirect("login")
    

@login_required
def set_new_password(request):
    if request.method == "POST":
        form = SetPasswordForm(request.user, request.POST)
        if form.is_valid():
            messages.success(request,"Password updated successfully.")
            form.save()
            return redirect("profile",request.user.id)
    else:
        form = SetPasswordForm(request.user)
    context = {
        "form" : form
    }
    return render(request, "accounts/set-new-password.html",context)

@login_required
def user_dashboard(request,id):
    author = CustomUser.objects.get(id=id)
    blogs = Blog.objects.filter(author=author).prefetch_related("categories", "reviews")
    
    for blog in blogs:
        blog.avg_rating = blog.reviews.aggregate(avg=Avg("rating"))["avg"] or 0

    return render(request, "accounts/profile.html", {
        "author": author,
        "blogs": blogs,
    })

@login_required
def update_profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile",request.user.id)
    else:
        form = UserProfileForm(instance=user)

    return render(request, "accounts/update_profile.html", {"form": form})


@login_required
def change_password(request):
    user = request.user 
    if request.method == "POST":
        form = PasswordChangeForm(user,request.POST)
        if form.is_valid():
            messages.success(request,"Password changed successfully.")
            form.save()
            return redirect("profile",request.user.id)
    else:
        form = PasswordChangeForm(user)
    context = {
        "form" : form ,
        "type" : "change"
    }
    return render(request,"accounts/change-password.html",context)




    
