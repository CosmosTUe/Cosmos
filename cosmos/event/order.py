from cosmos.event.base import PretixService


class Order(PretixService):
    """
    HTTP request service for Pretix Order

    Reference: https://docs.pretix.eu/en/latest/api/resources/orders.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        organizer = kwargs.get("organizer")
        event = kwargs.get("event")
        if organizer is None or event is None:
            # If correct arguments do not exist, raise TypeError
            raise TypeError
        # Otherwise, continue with HTTP request
        return f"/api/v1/organizers/{organizer}/events/{event}/orders/"

    @classmethod
    def get_all(cls, organizer, event: dict, email=None, **kwargs):
        """
        Performs a GET request for all orders of an event

        :param organizer: Name of organizer
        :param event: Dictionary detailing properties of Event
        :param email: Email (optional)
        :param kwargs:
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        data = super().get_all(organizer=organizer, event=event["slug"], email=email, **kwargs)
        return data if data["count"] > 0 else []
