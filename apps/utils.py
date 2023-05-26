import math

from django.core.validators import ValidationError
from django.utils.deconstruct import deconstructible


@deconstructible
class AspectRatioValidator:
    """
    Validator for the aspect ratio of an image.

    Must be initialized with the desired aspect
    ratio and can then be called with an image.
    """

    def __init__(self, ratio):
        self.ratio = ratio

    def __call__(self, image):
        if not math.isclose(image.width / image.height, self.ratio, rel_tol=1e-6):
            raise ValidationError("The aspect ratio is not correct. The aspect ratio should be: " + str(self.ratio))
