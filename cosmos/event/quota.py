from cosmos.event.base import PretixService


class Quota(PretixService):
    """
    HTTP request service for Pretix Quota

    Reference: https://docs.pretix.eu/en/latest/api/resources/quotas.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        """
        Defines the URL of HTTP request

        :param organizer: Name of organizer
        :param event: Name of event
        :param id: ID of quota (Optional)
        :param kwargs: Dictionary of arguments
        :return: HTTP request URL
        """
        organizer = kwargs.get("organizer")
        event = kwargs.get("event")
        if organizer is None or event is None:
            raise TypeError
        id = kwargs.get("id", "")
        return f"/api/v1/organizers/{organizer}/events/{event}/quotas/{id}"
