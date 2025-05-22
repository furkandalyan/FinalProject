from django.db import models
from django.db import models
from django.contrib.auth.models import User



class ZamanTakibi(models.Model):
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)
    baslangic = models.DateTimeField()
    bitis = models.DateTimeField()

    def __str__(self):
        return self.baslik
from django.db import models


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

from django.db import models

class Experience(models.Model):
    name = models.CharField(max_length=100)
    photo_url = models.URLField(default="https://randomuser.me/api/portraits/lego/1.jpg")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

from django.db import models
from django.contrib.auth.models import User

class TaskPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    suggestions = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)  # 🔧 yeni eklendi

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

