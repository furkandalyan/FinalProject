from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib import messages
from .models import Experience, BlogPost, TaskPrompt
from .forms import BlogPostForm, ExperienceForm
import json
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import TaskPrompt
from datetime import datetime, timedelta
from .forms import UserUpdateForm, ProfilePicForm
from django.utils.timezone import now
# Anasayfa
def index(request):
    experiences = list(Experience.objects.order_by('?')[:30].values('name', 'photo_url', 'content'))
    return render(request, 'yonetim/index.html', {'experiences': experiences})

# Kayıt
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('user_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'yonetim/register.html', {'form': form})

# Giriş
def login_view(request):
    return render(request, 'yonetim/login.html')

# Sekme kapanınca çıkış
def force_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return JsonResponse({"status": "logged_out"})

# Sayfalar
def our_purpose(request):
    return render(request, 'yonetim/our_purpose.html')

def contact(request):
    return render(request, 'yonetim/contact.html')

def faq(request):
    faq_list = [
        ("What is FinalProject?",
         "FinalProject is a platform designed to help users manage tasks, share experiences, and track productivity."),
        ("How can I register?", "Click the Register button on the top right corner and fill in the required details."),
        ("Can I use FinalProject for free?", "Yes, FinalProject is completely free to use."),
        ("How do I reset my password?", "Go to the login page and click on 'Forgot Password' to reset your password."),
        ("What kind of tasks can I manage?",
         "You can manage personal, academic, or professional tasks — anything you like."),
        ("How can I edit my profile information?",
         "Navigate to the Profile Settings page from the top menu after logging in."),
        ("Can I upload a profile picture?", "Yes, you can upload a profile picture in the Profile Settings section."),
        ("How does the task suggestion feature work?",
         "You submit a routine or problem, and the system suggests tasks using smart logic."),
        ("Is my data safe?", "Yes, your data is securely stored and not shared with third parties."),
        ("Can I delete my account?", "Yes, please contact support via the Contact page to request account deletion."),
        ("What is the 'Experience' section?",
         "It's a place to share your learning or productivity experiences with others."),
        ("Can I view blog posts without logging in?", "Yes, all public blog posts are visible to everyone."),
        ("How can I write a blog post?", "Login and go to the 'Create Blog Post' section under the Blog menu."),
        ("Can I edit my blog post later?", "Yes, go to 'My Blog Posts' to edit or delete your submissions."),
        ("How do I submit an experience?", "Go to the 'Share Experience' section and fill out the form."),
        ("Can I see my past task submissions?", "Yes, navigate to 'My Task Submissions' from the dashboard."),
        ("Are there any limitations on blog content?", "Yes, content must be respectful, appropriate, and original."),
        ("Is there a dark mode?", "Currently not, but we plan to support it in future updates."),
        ("Can I contact the developers?", "Yes, use the Contact page to reach out to the team."),
        ("What should I do if I find a bug?", "Please report any bugs via the Contact form with details.")
    ]

    return render(request, 'yonetim/faq.html', {'faq_list': faq_list})

def about_us(request):
    return render(request, 'yonetim/about_us.html')

def blog(request):
    blogs = BlogPost.objects.all().order_by('-created_at')  # Artık sınır yok

    for blog in blogs:
        if hasattr(blog.author, 'userprofile') and blog.author.userprofile.profile_pic:
            blog.author_image = blog.author.userprofile.profile_pic.url
        else:
            blog.author_image = '/static/default_profile.png'

    return render(request, 'yonetim/blog.html', {'blogs': blogs})



def user_experience(request):
    experiences = Experience.objects.all().order_by('-created_at')
    return render(request, 'yonetim/user_experience.html', {'experiences': experiences})

def home(request):
    if request.user.is_authenticated:
        return render(request, 'yonetim/user_base.html')
    else:
        return render(request, 'yonetim/guest_base.html')

@login_required
def user_dashboard(request):
    return render(request, 'yonetim/user_dashboard.html')

def logout_view(request):
    logout(request)
    return render(request, 'yonetim/logout_redirect.html')

# Görevler
@login_required
def my_tasks(request):
    prompts = TaskPrompt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'yonetim/task_prompt_list.html', {'prompts': prompts})

@login_required
def completed_tasks(request):
    prompts = TaskPrompt.objects.filter(user=request.user, is_completed=True).order_by('-created_at')
    return render(request, 'yonetim/completed_tasks.html', {'prompts': prompts})

@login_required
def mark_task_completed(request, prompt_id):
    prompt = get_object_or_404(TaskPrompt, id=prompt_id, user=request.user)
    prompt.is_completed = True
    prompt.save()
    return redirect('my_tasks')

@login_required
def task_statistics(request):
    return render(request, 'yonetim/task_statistics.html')

def productivity_reports(request):
    return render(request, 'yonetim/productivity_reports.html')

def latest_posts(request):
    blogs = BlogPost.objects.all().order_by('-created_at')[:5]
    return render(request, 'yonetim/latest_posts.html', {'blogs': blogs})

def my_blog_posts(request):
    posts = BlogPost.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'yonetim/my_blog_posts.html', {'posts': posts})

def create_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            messages.success(request, "✅ Blog post successfully submitted!")
            form = BlogPostForm()
    else:
        form = BlogPostForm()
    return render(request, 'yonetim/create_post.html', {'form': form})

@login_required
def blog_post_detail(request, pk):
    post = get_object_or_404(BlogPost, pk=pk)
    return render(request, 'yonetim/blog_post_detail.html', {'post': post})


from django.core.files.base import ContentFile
import base64

@login_required
def profile_settings(request):
    user_form = UserUpdateForm(instance=request.user)
    profile_form = ProfilePicForm(instance=request.user.userprofile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfilePicForm(request.POST, request.FILES, instance=request.user.userprofile)

        # Eğer kırpılmış görsel geldiyse
        cropped_file = request.FILES.get('profile_pic')

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()

            if cropped_file:
                request.user.userprofile.profile_pic = cropped_file
                request.user.userprofile.save()

            messages.success(request, "✅ Profile updated successfully.")
            return redirect('profile_settings')

    return render(request, 'yonetim/profile_settings.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })



def account_security(request):
    return render(request, 'yonetim/account_security.html')

def notification_settings(request):
    return render(request, 'yonetim/notification_settings.html')

def user_experiences(request):
    return render(request, 'yonetim/user_experiences.html')

@login_required
def submit_experience(request):
    form = ExperienceForm()
    success = False

    if request.method == 'POST':
        form = ExperienceForm(request.POST)
        if form.is_valid():
            experience = form.save(commit=False)

            # ✅ Eğer kullanıcı giriş yaptıysa ve profil fotoğrafı varsa, onu ata
            if hasattr(request.user, 'userprofile') and request.user.userprofile.profile_pic:
                experience.photo_url = request.user.userprofile.profile_pic.url

            experience.save()
            success = True
            form = ExperienceForm()  # formu temizle

    return render(request, 'yonetim/submit_experience.html', {'form': form, 'success': success})


def experience_tips(request):
    return render(request, 'yonetim/experience_tips.html')

def send_welcome_email(user):
    subject = 'Welcome to Tempus Naviga!'
    from_email = 'tempusnaviga@gmail.com'
    to_email = [user.email]
    html_content = render_to_string('emails/welcome_email.html', {'user': user})
    text_content = 'Welcome to Tempus Naviga!'
    email = EmailMultiAlternatives(subject, text_content, from_email, to_email)
    email.attach_alternative(html_content, "text/html")
    email.send()

def all_blogs(request):
    blogs = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'yonetim/all_blogs.html', {'blogs': blogs})

def experience_data(request):
    data = list(Experience.objects.order_by('-created_at')[:50].values('name', 'photo_url', 'content'))
    return JsonResponse(data, safe=False)

@login_required
def shared_experiences(request):
    experiences = Experience.objects.order_by('-created_at')[:50]
    return render(request, 'yonetim/shared_experiences.html', {'experiences': experiences})

@login_required
def request_task(request):
    suggestions = []
    input_text = ""
    success = False

    if request.method == "POST":
        input_text = request.POST.get("task_input", "").lower()

        # Öneriler
        if any(word in input_text for word in ["exercise", "workout", "gym", "run", "yoga"]):
            suggestions.append("🏋️ Consider scheduling 30 minutes of exercise every morning to boost energy.")
        if any(word in input_text for word in ["study", "homework", "exam", "learn"]):
            suggestions.append("📚 Use the Pomodoro technique: 50 minutes focused work, 10 minutes break.")
        if any(word in input_text for word in ["sleep", "late", "tired", "night"]):
            suggestions.append("🛌 Maintain a consistent sleep schedule to improve focus and energy.")
        if any(word in input_text for word in ["movie", "series", "tv", "netflix"]):
            suggestions.append("🎬 Limit screen time before bed; try reading for 15 minutes instead.")
        if any(word in input_text for word in ["meeting", "zoom", "call", "schedule"]):
            suggestions.append("📅 Review your calendar each morning to stay on top of your meetings.")
        if any(word in input_text for word in ["breakfast", "meal", "food", "snack"]):
            suggestions.append("🍽️ Plan healthy meals to stay energized throughout the day.")
        if any(word in input_text for word in ["procrastinate", "delay", "distract"]):
            suggestions.append("⏳ Try breaking tasks into small chunks to avoid procrastination.")
        if any(word in input_text for word in ["read", "book", "article"]):
            suggestions.append("📖 Set aside 20 minutes a day for reading to sharpen your mind.")
        if not suggestions:
            suggestions.append("🤖 I'm not sure what to suggest — try using more details or different keywords.")

        TaskPrompt.objects.create(
            user=request.user,
            message=input_text,
            suggestions=json.dumps(suggestions),
            created_at = now(),  # ⏰ Bunu ekledik
            is_completed = False

        )
        success = True
        input_text = ""

    return render(request, 'yonetim/request_task.html', {
        'success': success,
        'input_text': input_text
    })

@login_required
def task_prompt_list(request):
    prompts = TaskPrompt.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'yonetim/task_prompt_list.html', {'prompts': prompts})

@login_required
def task_prompt_detail(request, prompt_id):
    prompt = get_object_or_404(TaskPrompt, id=prompt_id, user=request.user)
    suggestions = json.loads(prompt.suggestions)
    return render(request, 'yonetim/task_prompt_detail.html', {
        'prompt': prompt,
        'suggestions': suggestions
    })


@login_required
def task_statistics(request):
    prompts = TaskPrompt.objects.filter(user=request.user)
    total = prompts.count()
    completed = prompts.filter(is_completed=True).count()
    pending = total - completed

    # Türlere göre analiz
    categories = {
        "Study": ["study", "exam", "homework", "school"],
        "Exercise": ["exercise", "gym", "run", "workout", "yoga"],
        "Sleep": ["sleep", "tired", "rest"],
        "Leisure": ["tv", "movie", "netflix", "game"],
        "Nutrition": ["food", "snack", "meal", "breakfast"]
    }

    category_stats = []

    for name, keywords in categories.items():
        category_prompts = prompts.filter(message__icontains=keywords[0])
        for k in keywords[1:]:
            category_prompts |= prompts.filter(message__icontains=k)

        cat_total = category_prompts.count()
        cat_completed = category_prompts.filter(is_completed=True).count()
        cat_percent = int((cat_completed / cat_total) * 100) if cat_total > 0 else 0

        category_stats.append({
            "name": name,
            "total": cat_total,
            "completed": cat_completed,
            "percent": cat_percent
        })

    context = {
        "total": total,
        "completed": completed,
        "pending": pending,
        "category_stats": category_stats
    }
    return render(request, "yonetim/task_statistics.html", context)



from datetime import datetime, timedelta
from django.utils.timezone import now
from django.db.models import Count
import json
from django.shortcuts import render
from .models import TaskPrompt

@login_required
def productivity_reports(request):
    tasks = TaskPrompt.objects.filter(user=request.user)
    total_tasks = tasks.count()
    completed_tasks = tasks.filter(is_completed=True).count()
    completion_rate = round((completed_tasks / total_tasks) * 100, 2) if total_tasks > 0 else 0
    last_submission = tasks.order_by('-created_at').first().created_at if total_tasks > 0 else None

    # En aktif gün
    most_active_day = tasks.extra(select={'day': "date(created_at)"}) \
                           .values('day') \
                           .annotate(count=Count('id')) \
                           .order_by('-count') \
                           .first()
    most_active_day_str = most_active_day['day'] if most_active_day else None
    most_active_day_count = most_active_day['count'] if most_active_day else 0

    # Son 7 gün verileri
    today = now().date()
    labels = []
    counts = []

    for i in range(6, -1, -1):  # 6 gün önce -> bugün
        day = today - timedelta(days=i)
        count = tasks.filter(created_at__date=day).count()
        labels.append(day.strftime('%a'))  # e.g., 'Mon'
        counts.append(count)

    recent_tasks = sum(counts)

    context = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'completion_rate': completion_rate,
        'last_submission': last_submission,
        'most_active_day': most_active_day_str,
        'most_active_day_count': most_active_day_count,
        'recent_tasks': recent_tasks,
        'daily_labels': json.dumps(labels),
        'daily_counts': json.dumps(counts),
    }

    return render(request, 'yonetim/productivity_reports.html', context)


from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

from django.contrib.auth.decorators import login_required
from .models import Notification

@login_required
def all_notifications(request):
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'yonetim/all_notifications.html', {'notifications': notifications})

from django.shortcuts import get_object_or_404, redirect

@login_required
def mark_notification_read(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.is_read = True
    notification.save()
    return redirect('all_notifications')

@login_required
def delete_notification(request, pk):
    notification = get_object_or_404(Notification, pk=pk, user=request.user)
    notification.delete()
    return redirect('all_notifications')
