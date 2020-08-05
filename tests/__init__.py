"""
Define test classes inside of __all__
"""
from .legacy import LegacyTestCase
from .user import UserForms, UserTestCase, UserViews

__all__ = ["UserForms", "UserTestCase", "UserViews", "LegacyTestCase"]
