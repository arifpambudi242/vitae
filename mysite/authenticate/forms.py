from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

# The get_user_model() function returns the currently used User Model as defined in the settings.py.
User = get_user_model()


# Create a custom UserCreationForm which points to our own
# Auth User instead of the Base Auth User of Django
# Here inside class Meta, we have defined the model as our own User model.
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')


class SignUpForm(CustomUserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2', )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'address_1', 'address_2', 'suburb', 'postcode', 'state', 'country', 'phone')