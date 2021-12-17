from .auth import CosmosLoginFormTest
from .profile import PasswordUpdateFormTest, PreferencesUpdateFormTest, ProfileUpdateFormTest
from .registration import RegisterUserFormTest

__all__ = [
    "CosmosLoginFormTest",
    "ProfileUpdateFormTest",
    "PasswordUpdateFormTest",
    "PreferencesUpdateFormTest",
    "RegisterUserFormTest",
]
