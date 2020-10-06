from cosmos.event.event import Event
from cosmos.event.order import Order


class User:
    @classmethod
    def get_events(cls, organizer, email):
        """
        Gets the list of events subscribed by the user.

        :param organizer:
        :param email: Email of the user
        :return: List of tuples (events subscribed, order created) by the user
        """
        results = []
        for event in Event.get_all(organizer).get("results", []):
            order = Order.get_all(organizer, event, email)
            if order is not None:
                results.append((event, order["results"]))
        return results
