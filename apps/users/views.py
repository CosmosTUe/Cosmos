from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from formtools.wizard.views import SessionWizardView

# from apps.users.forms import MemberCreateForm, MemberUpdateForm, ProfileCreateForm, ProfileUpdateForm
from apps.users.forms.registration import RegisterFontysForm, RegisterTueForm, RegisterUserForm
from apps.users.models.user import InstitutionFontys, InstitutionTue
from apps.users.tokens import account_activation_token


def show_tue_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step("register_user") or {}
    return cleaned_data.get("username", "None").endswith("tue.nl")


def show_fontys_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step("register_user") or {}
    return cleaned_data.get("username", "None").endswith("fontys.nl")


FORMS = [
    ("register_user", RegisterUserForm),
    ("register_tue", RegisterTueForm),
    ("register_fontys", RegisterFontysForm),
]

TEMPLATES = {
    "register_user": "user/register_user.html",
    "register_tue": "user/register_tue.html",
    "register_fontys": "user/register_fontys.html",
}

CONDITION_DICT = {
    "register_tue": show_tue_form_condition,
    "register_fontys": show_fontys_form_condition,
}


class RegistrationWizard(SessionWizardView):
    def done(self, form_list, form_dict, **kwargs):
        user_form = form_dict["register_user"]
        if user_form.cleaned_data["username"].endswith("tue.nl"):
            institution_form = form_dict["register_tue"]
        else:
            institution_form = form_dict["register_fontys"]

        if user_form.is_valid() and institution_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()

            profile = user.profile

            if user_form.cleaned_data["username"].endswith("tue.nl"):
                institution = InstitutionTue.objects.get(profile=profile)
                institution.department = institution_form.cleaned_data["department"]
                institution.program = institution_form.cleaned_data["program"]
                institution.save()
            else:
                institution = InstitutionFontys.objects.get(profile=profile)
                institution.study = institution_form.cleaned_data["study"]
                institution.save()

        # send_confirmation_email_task.delay(profile.id)

        return redirect(reverse("cosmos_users:registration_done"))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.Objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse("Thank you for your email confirmation. Now you can login your account.")
    else:
        return HttpResponse("Activation link is invalid!")


def registration_done(request):
    return render(request, "user/register_done.html")

# @login_required
# @transaction.atomic
# def profile(request):
#    """
#    Process User profile form.
#
#    - @login_required: Ensures authenticated user
#    - @transaction.atomic: Ensures both queries to the database are transactions
#
#    :param request:
#    :return:
#    """
#    if request.method == "POST":
#
#        user_form = MemberUpdateForm(data=request.POST, instance=request.user)
#        profile_form = ProfileUpdateForm(data=request.POST, instance=request.user.profile)
#        password_form = PasswordChangeForm(data=request.POST, user=request.user)
#
#        if "save_profile" in request.POST:
#            if user_form.is_valid() and profile_form.is_valid():
#                user_form.save()
#                profile_form.save()
#                messages.success(request, "Your profile was successfully updated!")
#                return redirect(reverse("cosmos_users:user_profile") + "#profile")
#        elif "save_password" in request.POST:
#            if password_form.is_valid():
#                password_form.save()
#                messages.success(request, "Your password was succesfully updated!")
#                return redirect(reverse("cosmos_users:user_profile") + "#password")
#        elif "save_preferences" in request.POST:
#            if profile_form.is_valid():
#                profile_form.save()
#                messages.success(request, "Your preferences were succesfully updated!")
#                return redirect(request("cosmos_users:user_profile") + "#preferences")
#        elif "save_key_access" in request.POST:
#            if profile_form.is_valid():
#                profile_form.save()
#                messages.success(request, "Your key access settings were succesfully updated!")
#                return redirect(reverse("cosmos_users:user_profile") + "#key-access")
#
#        if user_form.is_valid() and profile_form.is_valid():
#            user_form.save()
#            profile_form.save()
#            messages.success(request, "Your profile was successfully updated!")
#            return redirect("/")
#        else:
#            messages.error(request, "Please correct the error below.")
#    else:
#        user_form = MemberUpdateForm(instance=request.user)
#        profile_form = ProfileUpdateForm(instance=request.user.profile)
#        password_form = PasswordChangeForm(user=request.user)
#    return render(
#        request,
#        "user/profile.html",
#        {"user_form": user_form, "profile_form": profile_form, "password_form": password_form},
#    )


@login_required
def delete(request):
    if request.method == "POST":
        User.objects.get(username=request.user.username).delete()
    return redirect("/")
