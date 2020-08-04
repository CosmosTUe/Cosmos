"""
Define test classes inside of __all__
"""
from .user import UserForms, UserTestCase, UserViews
from .legacy import LegacyTestCase

__all__ = ["UserForms", "UserTestCase", "UserViews", "LegacyTestCase"]
