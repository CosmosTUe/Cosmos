from cosmos.event.base import PretixService


class Quota(PretixService):
    """
    HTTP request service for Pretix Quota

    Reference: https://docs.pretix.eu/en/latest/api/resources/quotas.html
    """

    @classmethod
    def _get_request_url(cls, **kwargs):
        organizer = kwargs.get("organizer")
        event = kwargs.get("event")
        id = kwargs.get("id", "")
        if organizer is None or event is None:
            raise TypeError
        return f"/api/v1/organizers/{organizer}/events/{event}/quotas/{id}"


if __name__ == "__main__":
    print(Quota.get_all(organizer="cosmos", event="potluck1"))
