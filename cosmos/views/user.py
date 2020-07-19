from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.db import transaction
from django.shortcuts import redirect, render

from cosmos.forms import ProfileChangeForm, ProfileCreationForm


def register(request):
    """
    Process User registration form

    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = UserCreationForm(request.POST, instance=request.user)
        profile_form = UserCreationForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Account created successfully")
            return redirect("register")
    else:
        user_form = UserCreationForm()
        profile_form = ProfileCreationForm()
    return render(request, "user/register.html", {"user_form": user_form, "profile_form": profile_form})


@login_required
@transaction.atomic
def update(request):
    """
    Process User update form.

    - @login_required: Ensures authenticated user
    - @transaction.atomic: Ensures both queries to the database are transactions

    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileChangeForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("settings:profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = ProfileChangeForm(instance=request.user.profile)
    return render(request, "user/update.html", {"user_form": user_form, "profile_form": profile_form})
