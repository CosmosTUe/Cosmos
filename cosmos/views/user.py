from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import redirect, render

from cosmos.forms import MemberCreateForm, MemberUpdateForm, ProfileCreateForm, ProfileUpdateForm


def register(request):
    """
    Process User registration form

    :param request:
    :return:
    """
    if request.method == "POST":
        user_form = MemberCreateForm(request.POST, instance=request.user)
        profile_form = ProfileCreateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Account created successfully")
            return redirect("register")
    else:
        user_form = MemberCreateForm()
        profile_form = ProfileCreateForm()
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
        user_form = MemberUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile was successfully updated!")
            return redirect("settings:profile")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = MemberUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "user/update.html", {"user_form": user_form, "profile_form": profile_form})
