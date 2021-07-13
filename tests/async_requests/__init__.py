"""
Define test classes inside of __all__
"""
from .commands import CommandsTestCase
from .executor import ExecutorTestCase
from .newsletter import NewsletterTestCase

__all__ = ["CommandsTestCase", "ExecutorTestCase", "NewsletterTestCase"]
