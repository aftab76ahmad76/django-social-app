from django.db.models.signals import post_save, pre_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile, Relationship


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_update_friends(sender, instance, created, **kwargs):
    _sender = instance.sender
    _receiver = instance.reciever
    if instance.status == "accepted":
        _sender.friends.add(_receiver.user)
        _receiver.friends.add(_sender.user)
        _sender.save()
        _receiver.save()


@receiver(pre_delete, sender=Relationship)
def pre_delete_remove_friends(sender, instance, **kwargs):
    sender = instance.sender
    reciever = instance.reciever
    sender.friends.remove(reciever.user)
    reciever.friends.remove(sender.user)
    sender.save()
    reciever.save()
