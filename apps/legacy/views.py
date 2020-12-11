# from django.contrib import messages
# from django.http import HttpResponse
# from django.shortcuts import redirect, render
# from django.utils.encoding import force_text
# from django.utils.http import urlsafe_base64_decode

# from apps.legacy.models import AuthUser
# from apps.legacy.tokens import account_import_token
# from apps.users.forms import MemberCreateForm, ProfileCreateForm
# from apps.users.models.user import Profile


# def import_user(request, uidb64, token):
#     """
#     View which handles the importing of the legacy user to the new website. Uses the information
#     from the unique link to determine the user and verifies this link belongs to them using the
#     token. Redirects the user to the account creation page with filled in information, as there
#     may be stricter requirements on the supplied information, and a new password needs to be
#     chosen.
#     """
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         old_user = AuthUser.objects.get(username=uid)
#     except (TypeError, ValueError, OverflowError, AuthUser.DoesNotExist):
#         old_user = None

#     if (
#         old_user is not None
#         and account_import_token.check_token(old_user, token)
#         and not Profile.objects.filter(user__username=uid).exists()
#     ):
#         if request.method == "POST":
#             user_form = MemberCreateForm(request.POST, instance=request.user)
#             profile_form = ProfileCreateForm(request.POST, instance=request.user.profile)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.succes(request, "Account imported succesfully!")
#                 return redirect("import_user")
#         else:
#             user_data = {
#                 "first_name": old_user.first_name,
#                 "last_name": old_user.last_name,
#                 "username": old_user.username,
#                 "email": old_user.email,
#             }
#             profile_data = {
#                 "nationality": old_user.mysiteprofile.nationality,
#                 "department": old_user.mysiteprofile.department,
#                 "program": old_user.mysiteprofile.program,
#             }
#             user_form = MemberCreateForm(initial=user_data)
#             profile_form = ProfileCreateForm(initial=profile_data)
#         return render(request, "user/register.html", {"user_form": user_form, "profile_form": profile_form})
#     else:
#         return HttpResponse("Account import link is invalid!")
