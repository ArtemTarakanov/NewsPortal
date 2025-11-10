import logging
from datetime import timedelta
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution

from news.models import Category, Post

logger = logging.getLogger(__name__)


def send_weekly_digest():
    """Еженедельная рассылка новых статей подписчикам"""
    # Находим все статьи за последнюю неделю
    week_ago = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(date_creation__gte=week_ago)
    
    if not new_posts.exists():
        logger.info("Нет новых статей за неделю")
        return
    
    # Для каждой категории отправляем письмо подписчикам
    for category in Category.objects.all():
        posts_in_category = new_posts.filter(categories=category)
        
        if not posts_in_category.exists():
            continue
            
        subscribers = category.subscribers.all()
        
        for subscriber in subscribers:
            # Формируем HTML контент
            html_content = render_to_string(
                'email/weekly_digest.html',
                {
                    'posts': posts_in_category,
                    'category': category,
                    'username': subscriber.username,
                }
            )
            
            # Отправляем письмо
            msg = EmailMultiAlternatives(
                subject=f'Еженедельная подборка новых статей в категории {category.name}',
                body='',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[subscriber.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            logger.info(f"Отправлено письмо для {subscriber.email}")
    
    logger.info(f"Еженедельная рассылка отправлена. Новых статей: {new_posts.count()}")


def delete_old_job_executions(max_age=604_800):
    """Удаляем старые задачи"""
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs APScheduler for weekly digest"

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")
        
        # Еженедельная рассылка по понедельникам в 9:00
        scheduler.add_job(
            send_weekly_digest,
            trigger=CronTrigger(day_of_week="mon", hour=9, minute=0),
            id="send_weekly_digest",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added job 'send_weekly_digest'.")

        # Удаление старых задач
        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(day_of_week="mon", hour=0, minute=0),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'delete_old_job_executions'.")

        try:
            logger.info("Starting scheduler...")
            scheduler.start()
        except KeyboardInterrupt:
            logger.info("Stopping scheduler...")
            scheduler.shutdown()
            logger.info("Scheduler shut down successfully!")