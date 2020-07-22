from datetime import datetime

import pytz

from cosmos.event.base import PretixService


class Event(PretixService):
    """
    HTTP request service for Pretix Event

    Reference: https://docs.pretix.eu/en/latest/api/resources/events.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        """
        Defines the URL of HTTP request

        :param organizer: Name of organizer
        :param kwargs: Dictionary of arguments
        :return: HTTP request URL
        """
        organizer = kwargs.get("organizer")
        if organizer is None:
            # If organizer does not exist, raise TypeError
            raise TypeError
        # Otherwise, continue with HTTP request
        event_name = kwargs.get("event", "")
        return f"/api/v1/organizers/{organizer}/events/{event_name}"

    @classmethod
    def get_all(cls, organizer, **kwargs):
        """
        Performs a GET request for all of the events under a certain organizer

        :param organizer: Name of organizer
        :param kwargs: Dictionary of queries
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().get_all(organizer=organizer)

    @classmethod
    def get(cls, organizer, event, **kwargs):
        """
        Performs a GET requeest for event information

        :param organizer: Name of organizer
        :param event: Name of event
        :param kwargs:
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().get_all(organizer=organizer, event=event)

    @classmethod
    def create(cls, organizer, name, date_from: datetime, timezone="Europe/Amsterdam", **kwargs):
        """
        Performs a POST request to create a new event under a certain organizer

        :param organizer: Name of organizer
        :param name: Name of event
        :param date_from: `datetime` object denoting the start point of the event
        :param timezone: Timezone of the event (defaults to "Europe/Amsterdam")
        :param kwargs: Additional properties of new event
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        date_to = kwargs.get("date_to")
        if date_to is not None:
            date_to = f"{date_to.strftime('%Y-%m-%dT%H:%M:%S')}{pytz.timezone(timezone)}"

        slug = kwargs.get("slug")
        if slug is None:
            slug = name.replace(" ", "-").lower()

        payload_dict = {
            "name": {"en": name},
            "slug": slug,
            # If live is True, event is publicly available
            "live": False,
            # "testmode": False,
            "currency": "EUR",
            "date_from": date_from,
            "date_to": date_to,
            # If is_public is True, event is available for all
            # If is_public is False, event is members-only
            "is_public": False,
            "seat_category_mapping": {},
            # TODO process location - dictionary to location, geo_lat, geo_lon?
            # "location": location,
            # "geo_lat": None,
            # "geo_lon": None,
            "timezone": timezone,
            "plugins": [
                "pretix.plugins.sendmail",
                "pretix.plugins.statistics",
                # TODO choose payment plugin
                # "pretix.plugins.mollie"
                # "pretix.plugins.stripe"
            ],
        }

        return super().create(organizer, **payload_dict)

    @classmethod
    def update(cls, organizer, event, **kwargs):
        """
        Performs a PATCH request

        :param organizer: Name of organizer
        :param event: Name of event
        :param kwargs: Properties of event to modify
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().update(organizer, event=event, **kwargs)

    @classmethod
    def delete(cls, organizer, event):
        """
        Performs a DELETE request to delete an event

        :param organizer: Name of organizer
        :param event: Name of event
        :returns: Response given as dictionary
        :raises PretixException: Request exception
        """
        return super().delete(organizer, event=event, id=id)
