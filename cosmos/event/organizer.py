from cosmos.event.base import PretixService


class Organizer(PretixService):
    """
    HTTP request service for Pretix Organizers

    Reference: https://docs.pretix.eu/en/latest/api/resources/organizers.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        """
        Defines the URL of HTTP request

        :param organizer: Name of organizer
        :param kwargs: Dictionary of arguments
        :return: HTTP request URL
        """
        organizer = kwargs.get("organizer", "")
        return f"api/v1/organizers/{organizer}"

    @classmethod
    def get_all(cls, **kwargs):
        """
        Returns a list of all organizers

        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().get_all(**kwargs)

    @classmethod
    def get(cls, organizer, **kwargs):
        """
        Returns information on one organizer account

        :param organizer: Name of organizer
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().get(organizer, **kwargs)

    @classmethod
    def create(cls, organizer, **kwargs):
        """
        Pretix Organizers do not support creation/POST requests
        """
        raise NotImplementedError

    @classmethod
    def update(cls, organizer, **kwargs):
        """
        Pretix Organizers do not support updating/PATCH requests
        """
        raise NotImplementedError

    @classmethod
    def delete(cls, organizer):
        """
        Pretix Organizers do not support deletions/DELETE requests
        """
        raise NotImplementedError


if __name__ == "__main__":
    print(Organizer.get_all())
