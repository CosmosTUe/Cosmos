from django.contrib import messages
from django.contrib.auth import authenticate, login
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
        user_form = MemberCreateForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            profile_form = ProfileCreateForm(request.POST, instance=user.profile)
            if profile_form.is_valid():
                user.profile = profile_form.save(user)
                messages.success(request, "Account created successfully")
                # Log in automatically
                raw_password = user_form.cleaned_data.get("password1")
                user = authenticate(username=user.username, password=raw_password)
                login(request, user)
                return redirect("/")
        else:
            profile_form = ProfileCreateForm(request.POST)
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
            return redirect("/")
        else:
            messages.error(request, "Please correct the error below.")
    else:
        user_form = MemberUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, "user/update.html", {"user_form": user_form, "profile_form": profile_form})
