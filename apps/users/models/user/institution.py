from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.models.user.constants import FONTYS_STUDIES, TUE_DEPARTMENTS, TUE_PROGRAMS
from apps.users.models.user.profile import Profile


class InstitutionTue(models.Model):

    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE)
    department = models.CharField(max_length=100, blank=False, choices=list(zip(TUE_DEPARTMENTS, TUE_DEPARTMENTS)))
    program = models.CharField(max_length=100, blank=False, choices=list(zip(TUE_PROGRAMS, TUE_PROGRAMS)))
    tue_id = models.CharField(verbose_name="TU/e Student Number", blank=True, max_length=25)
    card_number = models.CharField(max_length=25, blank=True)
    key_access = models.BooleanField(max_length=3, default=False)

    @property
    def username(self):
        return self.profile.user.username

    def __str__(self):
        return f"{self.username}"


class InstitutionFontys(models.Model):

    profile = models.OneToOneField(Profile, blank=True, on_delete=models.CASCADE)
    study = models.CharField(max_length=100, blank=False, choices=list(zip(FONTYS_STUDIES, FONTYS_STUDIES)))

    @property
    def username(self):
        return self.profile.user.username

    def __str__(self):
        return f"{self.username}"


@receiver(post_save, sender=Profile)
def profile_post_save(sender, instance: Profile, created, **kwargs):
    if created:
        if instance.user.username.endswith("tue.nl"):
            InstitutionTue.objects.create(profile=instance)
        elif instance.user.username.endswith("fontys.nl"):
            InstitutionFontys.objects.create(profile=instance)

    if instance.user.username.endswith("tue.nl"):
        InstitutionTue.objects.get(profile=instance).save()
    elif instance.user.username.endswith("fontys.nl"):
        InstitutionFontys.objects.get(profile=instance).save()
