import os
from io import BytesIO

from django.core.files import File
from PIL import Image

from cosmos.models import GMM


def get_new_file(name):
    if not os.path.exists("temp/"):
        os.mkdir("temp")
    with open(f"temp/{name}", "w") as test:
        test.write(" ")
    return open(f"temp/{name}", "rb")


def clear_temp_files():
    if not os.path.exists("temp/"):
        return

    for filename in os.listdir("temp/"):
        os.remove(f"temp/{filename}")
    os.removedirs("temp/")


def get_new_gmm(name="TestGMM", date="2010-10-21"):
    """
    Shortcut to create new default GMM object

    :param name:
    :param date:
    :return: GMM object
    """
    return GMM.objects.create(name=name, date=date)


# https://stackoverflow.com/questions/26298821/django-testing-model-with-imagefield
def get_image_file(name="test.png", ext="png", size=None, color=None):
    if size is None:
        size = (50, 50)
    if color is None:
        color = (256, 0, 0)
    file_obj = BytesIO()
    image = Image.new("RGB", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)
