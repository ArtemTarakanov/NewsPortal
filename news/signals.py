from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from .models import Post

@receiver(post_save, sender=Post)
def notify_subscribers(sender, instance, created, **kwargs):
    if created:  
        categories = instance.categories.all()
        
        for category in categories:
            subscribers = category.subscribers.all()
            
            for subscriber in subscribers:
                
                html_content = render_to_string(
                    'email/new_post.html',
                    {
                        'post': instance,
                        'username': subscriber.username,
                    }
                )
                
                
                send_mail(
                    subject=instance.title,  
                    message='',  
                    from_email=None,
                    recipient_list=[subscriber.email],
                    html_message=html_content,  
                )