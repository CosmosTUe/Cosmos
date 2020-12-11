"""
Configure Admin interface

Reference: `Django documentation <https://docs.djangoproject.com/en/3.0/ref/contrib/admin/>`_
"""
from .board import BoardAdmin
from .committee import CommitteeAdmin

__all__ = ["BoardAdmin", "CommitteeAdmin"]
