from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', auth_views.LoginView.as_view(template_name='yonetim/login.html'), name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('force-logout/', views.force_logout, name='force_logout'),

    # Bilgilendirme sayfaları
    path('our-purpose/', views.our_purpose, name='our_purpose'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
    path('about-us/', views.about_us, name='about_us'),

    # Blog
    path('blog/', views.blog, name='blog'),
    path('latest-posts/', views.latest_posts, name='latest_posts'),
    path('my-blog-posts/', views.my_blog_posts, name='my_blog_posts'),
    path('my-blog-posts/<int:pk>/', views.blog_post_detail, name='blog_post_detail'),
    path('create-post/', views.create_post, name='create_post'),
    path('all-blogs/', views.all_blogs, name='all_blogs'),

    # Experience
    path('user-experience/', views.user_experience, name='user_experience'),
    path('user-experiences/', views.user_experiences, name='user_experiences'),
    path('submit-experience/', views.submit_experience, name='submit_experience'),
    path('experience-tips/', views.experience_tips, name='experience_tips'),
    path('shared-experiences/', views.shared_experiences, name='shared_experiences'),
    path('api/experiences/', views.experience_data, name='experience_data'),

    # Kullanıcı
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile-settings/', views.profile_settings, name='profile_settings'),
    path('account-security/', views.account_security, name='account_security'),
    path('notification-settings/', views.notification_settings, name='notification_settings'),

    # Görevler
    path('my-tasks/', views.task_prompt_list, name='my_tasks'),
    path('completed-tasks/', views.completed_tasks, name='completed_tasks'),
    path('task-detail/<int:prompt_id>/', views.task_prompt_detail, name='task_prompt_detail'),
    path('mark-task-completed/<int:prompt_id>/', views.mark_task_completed, name='mark_task_completed'),
    path('task-statistics/', views.task_statistics, name='task_statistics'),
    path('productivity-reports/', views.productivity_reports, name='productivity_reports'),
    path('request-task/', views.request_task, name='request_task'),
    path('all-notifications/', views.all_notifications, name='all_notifications'),
    path('mark-notification-read/<int:pk>/', views.mark_notification_read, name='mark_notification_read'),

    path('delete-notification/<int:pk>/', views.delete_notification, name='delete_notification'),

]
