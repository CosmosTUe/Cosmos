from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.users.helper_functions import is_fontys_email, is_tue_email
from apps.users.models.constants import FONTYS_STUDIES, TUE_DEPARTMENTS, TUE_PROGRAMS
from apps.users.models.profile import Profile


class Institution(models.Model):
    profile = models.OneToOneField(Profile, blank=False, on_delete=models.CASCADE)

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.username}"

    @property
    def username(self):
        return self.profile.user.username


class InstitutionTue(Institution):
    department = models.CharField(max_length=100, blank=False, choices=list(zip(TUE_DEPARTMENTS, TUE_DEPARTMENTS)))
    program = models.CharField(max_length=100, blank=False, choices=list(zip(TUE_PROGRAMS, TUE_PROGRAMS)))

    class Meta:
        verbose_name = "Member of TU/e"
        verbose_name_plural = "Members of TU/e"

    def __str__(self):
        return "Institute - TU/e"


class InstitutionFontys(Institution):
    study = models.CharField(max_length=100, blank=False, choices=list(zip(FONTYS_STUDIES, FONTYS_STUDIES)))

    class Meta:
        verbose_name = "Member of Fontys"
        verbose_name_plural = "Members of Fontys"

    def __str__(self):
        return "Institute - Fontys"


@receiver(post_save, sender=Profile)
def profile_post_save(sender, instance: Profile, created, **kwargs):
    username = instance.user.username
    if is_tue_email(username):
        institution_model = InstitutionTue
    elif is_fontys_email(username):
        institution_model = InstitutionFontys
    else:
        # TODO raise exception?
        return

    if created:
        institution_model.objects.create(profile=instance)
    institution_model.objects.get(profile=instance).save()
