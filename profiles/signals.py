# signals? Some kinds of communication system 
# Sender sends notis of actions 
# base on that info, recievers do proper work

from .models import Profile
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    # Only if when the instance is created. then this function should work!
    

    # Let's see it in real
    print(sender)   # <class 'django.contrib.auth.models.User'>
    print(instance) # testuser
    print(created)  # True



    if created:
        Profile.objects.create(user = instance)