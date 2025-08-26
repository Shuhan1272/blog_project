from django.contrib.auth.models import AbstractUser
from django.db import models
from .managers import CustomUserManager 
from django.utils.text import slugify


class CustomUser(AbstractUser): #inherit AbstractUser #Creating CustomUser model #Note : Must be register in settings the changes 
    role_choices = (
        ('admin', 'Admin'),
        ('author', 'Author'),
        ('reader', 'Reader')
    )
    role = models.CharField(max_length=10, choices=role_choices, default='author')
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    agreed_t_and_c = models.BooleanField(default=False)

    bio = models.TextField(blank=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)

    #by default null is false , if i give null = true and then don't give data then when I will access the data I will get None 
    address_line_1 = models.CharField(blank=True, max_length=100) #can be null in database , blank is only for admin panel. 
    address_line_2 = models.CharField(blank=True, max_length=100)
    city = models.CharField(blank=True, max_length=20)
    postcode = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    mobile = models.CharField(blank=True, max_length=15)

    profile_picture = models.ImageField(null=True, blank=True, upload_to="user_profile") #one folder will be created inside media/user_profile/abc.jpg 

    USERNAME_FIELD = "email" #Now our username field is email , override parent behaivour 
    REQUIRED_FIELDS = [] #USERNAME_FIELD is already a required field , so , no need to say again REQUIRED_FIELDS ['email'] that is making blank 

    username = models.CharField(max_length=150,default="user") #username is still required field in AbstractUser so we are providing default value as email

 
    objects = CustomUserManager()

    @property
    def full_name(self):
        if self.first_name == "" and self.last_name == "":
            return f"{self.username}{self.id}"
        return f"{self.first_name}  {self.last_name}"
    @property
    def full_address(self): #method for getting full address x + y 
        return f"{self.address_line_1} {self.address_line_2}"
