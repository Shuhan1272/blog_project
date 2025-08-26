from django.contrib import admin

# Register your models here.

from .models import CustomUser 

#issue : when we change password in admin panel , password was plain text, so we need hashed password in admin panel. 
#solution : we will override the save_model method which is inside admin.ModelAdmin class. 
#if the form has field name with password we will hashed the password 
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if form.cleaned_data.get("password"):
            obj.set_password(form.cleaned_data["password"])
        return super().save_model(request,obj,form,change)
    
