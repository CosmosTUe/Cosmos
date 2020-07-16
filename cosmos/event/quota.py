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
        pass

    @classmethod
    def get_all(cls, **kwargs):
        return super().get_all(**kwargs)

    @classmethod
    def get(cls, organizer, **kwargs):
        return super().get(organizer, **kwargs)

    @classmethod
    def create(cls, organizer, **kwargs):
        return super().create(organizer, **kwargs)

    @classmethod
    def update(cls, organizer, **kwargs):
        return super().update(organizer, **kwargs)

    @classmethod
    def delete(cls, organizer, **kwargs):
        return super().delete(organizer, **kwargs)


if __name__ == "__main__":
    print(Quota.get_all(organizer="cosmos", event="potluck1"))
