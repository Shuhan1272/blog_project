
from . models import CustomUser
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django import forms 

class CustomUserForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        label='First Name',
    )
    last_name = forms.CharField(
        required=True,
        label='Last Name',
    )
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','password1','password2','agreed_t_and_c']
        
    def clean_agreed_t_and_c(self):
        agreed = self.cleaned_data.get('agreed_t_and_c')
        if not agreed:
            raise forms.ValidationError("You must agree to the terms and conditions.")
        return agreed


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            "first_name", "last_name", "username", "email", 
            "bio", "twitter", "linkedin", "facebook",
            "address_line_1", "address_line_2", "city", "postcode", "country", "mobile",
            "profile_picture"
        ]
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 3}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField()

