from django import forms
from .models import Record

class SignupForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm password'})
    )

    class Meta:
        model = Record
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone',
            'address',
            'city',
            'state',
            'zip_code'
        ]
        # You could specify widgets or placeholders for each field if you want
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email address'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.TextInput(attrs={'placeholder': 'Address'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'zip_code': forms.TextInput(attrs={'placeholder': 'Zip code'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password1')
        p2 = cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        record = super().save(commit=False)
        record.password = self.cleaned_data['password1']  # plain-text password
        if commit:
            record.save()
        return record
