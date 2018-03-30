from django import forms

from .models import Post

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text')
username_regex_field = forms.RegexField(
    label='Username',
    max_length=30,
    regex=r'^[a-z0-9-_]+$',
    error_messages={
        'required': 'Please enter your name',
        'invalid': 'Lowercase alphanumeric characters and underscores and dashes only (a-z, 0-9, _, -)'
    },
)
password_char_field = forms.CharField(
    label='Password',
    max_length=30,
    widget=forms.PasswordInput,
)

confirm_password_char_field = forms.CharField(
    label='Confirm Password',
    max_length=30,
    widget=forms.PasswordInput,
)
class ProfileForm(forms.Form):
    username = username_regex_field
    first_name = forms.RegexField(
        label='First Name',
        max_length=30,
        regex=r'^[a-zA-Z-_]+$',
        error_messages={'invalid': 'Alphabetical, underscores, and dashes only (a-z, A-Z, _, -)'},
        required=False,
    )
    last_name = forms.RegexField(
        label='First Name',
        max_length=30,
        regex=r'^[a-zA-Z-_]+$',
        error_messages={'invalid': 'Alphabetical, underscores, and dashes only (a-z, A-Z, _, -)'},
        required=False,
    )
    email = forms.EmailField(
        label='First Name',
        max_length=50,
        required=False,
    )
    password = password_char_field
    confirm_password = confirm_password_char_field

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password and password != confirm_password:
            raise forms.ValidationError("Passwords don't match")

        return self.cleaned_data