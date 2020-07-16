from cosmos.event.event import Event
from cosmos.event.order import Order


class User:
    @classmethod
    def get_events(cls, organizer, email):
        """
        Gets the list of events subscribed by the user.

        :param organizer:
        :param email: Email of the user
        :return: List of events subscribed by the user
        """
        results = []
        for event in Event.get_all(organizer)[1].get("results", []):
            success, orders = Order.get_all(organizer, event, email)
            if success:
                results.append(event)
        return results


if __name__ == "__main__":
    print(User.get_events("cosmos", "dasyad00@gmail.com"))
