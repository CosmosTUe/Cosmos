from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from cosmos.forms import MemberCreateForm, ProfileCreateForm
from legacy.models import AuthUser
from legacy.tokens import account_import_token


def import_user(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        old_user = AuthUser.objects.get(username=uid)
    except (TypeError, ValueError, OverflowError, AuthUser.DoesNotExist):
        old_user = None

    if old_user is not None and account_import_token.check_token(old_user, token):
        if request.method == "POST":
            user_form = MemberCreateForm(request.POST, instance=request.user)
            profile_form = ProfileCreateForm(request.POST, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.succes(request, "Account imported succesfully!")
                return redirect("import_user")
        else:
            user_data = {
                "first_name": old_user.first_name,
                "last_name": old_user.last_name,
                "username": old_user.username,
                "email": old_user.email,
            }
            profile_data = {
                "nationality": old_user.mysiteprofile.nationality,
                "department": old_user.mysiteprofile.department,
                "program": old_user.mysiteprofile.program,
            }
            user_form = MemberCreateForm(initial=user_data)
            profile_form = ProfileCreateForm(initial=profile_data)
        return render(request, "user/register.html", {"user_form": user_form, "profile_form": profile_form})
    else:
        return HttpResponse("Account import link is invalid!")
