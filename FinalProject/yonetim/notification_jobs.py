from datetime import timedelta
from django.utils.timezone import now
from .models import TaskPrompt, Notification

def check_old_tasks_and_notify():
    timeframes = [
        (timedelta(days=365),  "🗓️ 1 year"),
        (timedelta(days=30),   "📆 1 month"),
        (timedelta(weeks=1),   "📅 1 week"),
        (timedelta(minutes=1), "⏱️ 1 minute"),  # test amaçlı
    ]

    current_time = now()

    for delta, label in timeframes:
        threshold = current_time - delta
        tasks = TaskPrompt.objects.filter(
            created_at__lte=threshold,
            is_completed=False
        )

        for task in tasks:
            # Eğer bu görev için halihazırda herhangi bir bildirim oluşturulduysa geç
            if Notification.objects.filter(
                    user=task.user,
                    reference__endswith=f"_task_{task.id}"
                ).exists():
                continue   # başka etikete geçme

            # Kullanıcıya gösterilecek mesaj
            display_message = (
                f"{label} ago you created a task but haven't completed it yet. "
                "Don't forget to finish it! 📝"
            )
            ref_key = f"{label}_task_{task.id}"

            Notification.objects.create(
                user=task.user,
                message=display_message,
                reference=ref_key
            )
