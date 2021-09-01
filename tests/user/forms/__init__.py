from .auth import CosmosLoginFormTest
from .profile import KeyAccessUpdateFormTest, PasswordUpdateFormTest, PreferencesUpdateFormTest, ProfileUpdateFormTest
from .registration import RegisterUserFormTest

__all__ = [
    "CosmosLoginFormTest",
    "ProfileUpdateFormTest",
    "PasswordUpdateFormTest",
    "PreferencesUpdateFormTest",
    "KeyAccessUpdateFormTest",
    "RegisterUserFormTest",
]
