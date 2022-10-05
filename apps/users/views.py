import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from formtools.wizard.views import SessionWizardView

from apps.async_requests.commands.subscribe_command import NewsletterSubscribeCommand
from apps.async_requests.commands.unsubscribe_command import NewsletterUnsubscribeCommand
from apps.async_requests.factory import Factory
from apps.users.forms.authorization import CosmosLoginForm
from apps.users.forms.profile import PasswordUpdateForm, PreferencesUpdateForm, ProfileUpdateForm
from apps.users.forms.registration import RegisterFontysForm, RegisterTueForm, RegisterUserForm
from apps.users.helper_functions import is_fontys_email, is_tue_email
from apps.users.mail import create_confirm_account_email
from apps.users.models import Board, Committee
from apps.users.models.institution import InstitutionFontys, InstitutionTue
from apps.users.tokens import account_activation_token

logger = logging.getLogger(__name__)
executor = Factory.get_executor()


def show_tue_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step("register_user") or {}
    return is_tue_email(cleaned_data.get("username", "None"))


def show_fontys_form_condition(wizard):
    cleaned_data = wizard.get_cleaned_data_for_step("register_user") or {}
    return is_fontys_email(cleaned_data.get("username", "None"))


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
        username = user_form.cleaned_data["username"]
        if is_tue_email(username):
            institution_form = form_dict["register_tue"]
        elif is_fontys_email(username):
            institution_form = form_dict["register_fontys"]
        else:
            # TODO raise exception?
            pass

        if user_form.is_valid() and institution_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = False
            user.save()
            user.refresh_from_db()

            profile = user.profile

            if is_tue_email(username):
                institution = InstitutionTue.objects.get(profile=profile)
                institution.department = institution_form.cleaned_data["department"]
                institution.program = institution_form.cleaned_data["program"]
                institution.save()
            elif is_fontys_email(username):
                institution = InstitutionFontys.objects.get(profile=profile)
                institution.study = institution_form.cleaned_data["study"]
                institution.save()
            else:
                # TODO raise exception?
                pass

            create_confirm_account_email(profile).send()

            if profile.subscribed_newsletter:
                email = user.username if profile.newsletter_recipient == "TUE" else user.email
                # TODO replace with django-newsletter
                executor.add_command(NewsletterSubscribeCommand(email, user.first_name, user.last_name))

        return redirect(reverse("cosmos_users:registration_done"))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]


def activate(request, uidb64, token):
    if request.method == "POST":
        try:
            username = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(username=username)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            return HttpResponse("Thank you for your email confirmation. Now you can login your account.")
        else:
            return HttpResponse("Activation link is invalid!")
    else:
        return render(request, "user/activate.html")


def registration_done(request):
    return render(request, "user/register_done.html")


@login_required
def profile(request):
    if request.method == "POST":

        profile_update_form = ProfileUpdateForm(data=request.POST, instance=request.user)
        password_change_form = PasswordUpdateForm(data=request.POST, user=request.user)
        preferences_update_form = PreferencesUpdateForm(data=request.POST, instance=request.user)

        if "save_profile" in request.POST:
            if profile_update_form.is_valid():
                profile_update_form.save()
                messages.success(request, "Your profile has been updated!")
                return redirect(reverse("cosmos_users:user_profile") + "#profile")
        elif "save_password" in request.POST:
            if password_change_form.is_valid():
                password_change_form.save()
                messages.success(request, "Your password has been updated!")
                return redirect(reverse("cosmos_users:user_profile") + "#password")
        elif "save_preferences" in request.POST:
            if preferences_update_form.is_valid():
                preferences_update_form.save()
                messages.success(request, "Your preferences have been updated!")
                return redirect(reverse("cosmos_users:user_profile") + "#preferences")

    else:
        profile_update_form = ProfileUpdateForm(instance=request.user)
        password_change_form = PasswordUpdateForm(user=request.user)
        preferences_update_form = PreferencesUpdateForm(instance=request.user)

    return render(
        request,
        "user/profile.html",
        {
            "profile_update_form": profile_update_form,
            "password_change_form": password_change_form,
            "preferences_update_form": preferences_update_form,
        },
    )


@login_required
def delete(request):
    if request.method == "POST":
        # Remove newsletter subscription before deleting the user
        executor.add_command(NewsletterUnsubscribeCommand(request.user.username))
        executor.add_command(NewsletterUnsubscribeCommand(request.user.email))
        User.objects.get(username=request.user.username).delete()
        messages.success(request, "Your account has successfully been deleted")
    return redirect("/")


def board_overview(request):
    boards = Board.objects.order_by("-period_from").all()
    return render(request, "boards/overview.html", {"boards": boards})


def committee_overview(request):
    committees = Committee.objects.all()
    return render(request, "committees/overview.html", {"committees": committees})


def committee_subpage(request, slug):
    committee = get_object_or_404(Committee, slug=str(slug))
    return render(request, "committees/subpage.html", {"committee": committee})


class CosmosLoginView(LoginView):
    form_class = CosmosLoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data["remember_me"]
        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        else:
            self.request.session.set_expiry(1209600)  # 2 weeks
            self.request.session.modified = True
        return super(CosmosLoginView, self).form_valid(form)
