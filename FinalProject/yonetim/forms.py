from django import forms
from django.contrib.auth.models import User
from .models import BlogPost, Experience, UserProfile

# Blog gönderisi formu
class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']

# Deneyim paylaşma formu
class ExperienceForm(forms.ModelForm):
    class Meta:
        model = Experience
        fields = ['name', 'photo_url', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'photo_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Profile Picture URL'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Share your experience...', 'rows': 5}),
        }

# Kullanıcı adı ve e-posta güncelleme formu
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

# Profil fotoğrafı güncelleme formu
class ProfilePicForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_pic']
