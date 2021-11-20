"""
------
README
------

Be sure to define each model in the database in `__all__`.

Reference: `Django Migration Documentation <https://docs.djangoproject.com/en/3.0/topics/migrations/>`_
"""
from apps.users.models.board import Board
from apps.users.models.committee import Committee
from apps.users.models.institution import InstitutionFontys, InstitutionTue
from apps.users.models.profile import Profile

__all__ = ["Board", "Committee", "Profile", "InstitutionFontys", "InstitutionTue"]
