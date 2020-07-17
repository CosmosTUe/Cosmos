from cosmos.event.base import PretixService


class Order(PretixService):
    """
    HTTP request service for Pretix Order

    Reference: https://docs.pretix.eu/en/latest/api/resources/orders.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        """
        Defines the URL of HTTP request

        :param organizer: Name of organizer
        :param event: Name of event
        :param code: Order code (Optional)
        :param kwargs: Dictionary of arguments
        :return: HTTP request URL
        """
        organizer = kwargs.get("organizer")
        event = kwargs.get("event")
        if organizer is None or event is None:
            # If correct arguments do not exist, raise TypeError
            raise TypeError
        # Otherwise, continue with HTTP request
        code = kwargs.get("code", "")
        return f"/api/v1/organizers/{organizer}/events/{event}/orders/{code}"

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

    @classmethod
    def get(cls, organizer, event, code):
        """
        Performs a GET request for information on one order

        :param organizer: Name of organizer
        :param event: Name of event
        :param code: Code of order
        """
        return super().get(organizer, event=event, code=code)
