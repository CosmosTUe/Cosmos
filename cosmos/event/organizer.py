from cosmos.event.base import PretixService


class Organizer(PretixService):
    """
    HTTP request service for Pretix Organizers

    Reference: https://docs.pretix.eu/en/latest/api/resources/organizers.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        organizer = kwargs.get("organizer", "")
        return f"api/v1/organizers/{organizer}"


if __name__ == "__main__":
    print(Organizer.get_all())
