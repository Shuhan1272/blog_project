from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse

#this confirms email is for favourite 
def send_confirmation_email(request, user,blog):
    blog_url = request.build_absolute_uri(
        reverse("blog_detail", args=[blog.slug])
    )

    email_subject = "Confirmation of Favorite Blog"
    email_body = render_to_string(
        "blog/confirmation_email.html",
        {"user" : user, "blog" : blog, "blog_url": blog_url},
    )

    email = EmailMessage( #here EmailMessage is a build in class 
        subject=email_subject,
        body=email_body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email],
    )

    email.content_subtype = "html" #Note : in email body if we pass html then this line is must. 
    email.send()