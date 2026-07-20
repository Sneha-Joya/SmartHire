from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, FreelancerProfile, ClientProfile


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    user_type = forms.ChoiceField(
        choices=User.USER_TYPE_CHOICES,
        widget=forms.RadioSelect,
        required=True
    )
    phone_number = forms.CharField(max_length=20, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 'phone_number', 'profile_picture')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.user_type = self.cleaned_data['user_type']
        user.phone_number = self.cleaned_data.get('phone_number', '')
        if self.cleaned_data.get('profile_picture'):
            user.profile_picture = self.cleaned_data['profile_picture']
        
        if commit:
            user.save()
            # Create profile based on user type
            if user.user_type == 'freelancer':
                FreelancerProfile.objects.create(user=user)
            elif user.user_type == 'client':
                ClientProfile.objects.create(user=user)
        
        return user


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = ['bio', 'hourly_rate', 'skills', 'portfolio_url', 'location', 'availability']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'hourly_rate': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Python, Django, JavaScript'}),
            'portfolio_url': forms.URLInput(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = ['company_name', 'company_description', 'location', 'website']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'website': forms.URLInput(attrs={'class': 'form-control'}),
        }

