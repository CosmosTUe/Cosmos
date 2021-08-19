import os

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
