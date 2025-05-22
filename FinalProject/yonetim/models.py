from django.db import models
from django.contrib.auth.models import User

# Zaman Takibi
class ZamanTakibi(models.Model):
    baslik = models.CharField(max_length=255)
    aciklama = models.TextField(blank=True, null=True)
    baslangic = models.DateTimeField()
    bitis = models.DateTimeField()

    def __str__(self):
        return self.baslik

# Blog
class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Experience
class Experience(models.Model):
    name = models.CharField(max_length=100)
    photo_url = models.URLField(default="https://randomuser.me/api/portraits/lego/1.jpg")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# Task Prompt
class TaskPrompt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    suggestions = models.TextField()
    created_at = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    category = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.created_at}"

# Kullanıcı Profili
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

    def __str__(self):
        return self.user.username

# 🔔 Bildirimler
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=255)
    reference = models.CharField(max_length=255, blank=True, null=True)  # ⬅ GİZLİ referans alanı
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"To: {self.user.username} | {self.message[:30]}..."

